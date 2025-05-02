from fastapi import APIRouter, Path, WebSocket
from fastapi.websockets import WebSocketDisconnect

from server.src.auth.utils import verify_access_token
from server.src.websocket.ConnectionManager import manager
from server.src.config import settings


router = APIRouter(
    tags=["Websockets"],
    prefix="/ws"
)


@router.websocket("/{room_id}")
async def ws_connect(
    websocket: WebSocket, 
    room_id: int = Path(),
):
    token = websocket.cookies.get(settings.JWT_ACCESS_TOKEN_COOKIE_NAME)
    user = await verify_access_token(token)
    user_id = int(user.get("sub"))
    user_name = str(user.get(settings.JWT_TOKEN_PAYLOAD_USERNAME_KEY))
    await manager.connect(
        websocket=websocket,
        room_id=room_id,
        user_id=user_id,
    )
    history = await manager.get_room_history(room_id=room_id)
    for message in reversed(history):
        message: dict
        await websocket.send_json({
            "text": message.get("text"),
            "is_self": message.get("sender_id") == user_id,
            "is_system": message.get("is_system"),
        })
    connection_message = f"User {user_name} connected"
    await manager.save_message(
        message=connection_message,
        room_id=room_id,
        sender_id=user_id,
        is_system=True,
    )
    await manager.broadcast(
        message=connection_message,
        room_id=room_id,
        sender_id=user_id,
        is_system=True,
    )
    try:
        while True:
            data = await websocket.receive_text()
            to_broadcast = f"{user_name}: {data}"
            await manager.save_message(
                message=to_broadcast,
                room_id=room_id,
                sender_id=user_id,
            )
            await manager.broadcast(
                message=to_broadcast,
                room_id=room_id,
                sender_id=user_id,
            )
    except WebSocketDisconnect:
        await manager.disconnect(
            room_id=room_id,
            user_id=user_id,
        )
        disconnection_message = f"User {user_name} disconnected"
        await manager.save_message(
            message=disconnection_message,
            room_id=room_id,
            sender_id=user_id,
            is_system=True
        )
        await manager.broadcast(
            message=disconnection_message,
            room_id=room_id,
            sender_id=user_id,
            is_system=True,
        )
