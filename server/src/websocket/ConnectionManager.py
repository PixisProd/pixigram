from typing import Dict, List
from dataclasses import dataclass, asdict
import json

from fastapi import WebSocket
import redis.asyncio as redis

from server.src.redis import get_redis_client
from server.src.websocket.schemas import WSMessage


class ConnectionManager():
    def __init__(self):
        self.redis: redis.Redis = get_redis_client()
        self.active_connections: Dict[int, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, room_id: str, user_id: int) -> None:
        await websocket.accept()
        self.active_connections[user_id] = websocket
        await self.redis.sadd(f"room:{room_id}", user_id)
    
    async def disconnect(self, room_id: str, user_id: int) -> None:
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        await self.redis.srem(f"room:{room_id}", user_id)
        if await self.redis.scard(f"room:{room_id}") == 0:
            await self.redis.delete(f"room:{room_id}:messages")
            await self.redis.delete(f"room:{room_id}")

    async def save_message(
            self,
            message: str,
            room_id: str, 
            sender_id: int,
            is_system: bool = False,
    ) -> None:
        message_class = WSMessage(
            text=message,
            sender_id=sender_id,
            is_system=is_system,
        )
        await self.redis.lpush(
            f"room:{room_id}:messages", 
            json.dumps(message_class.model_dump()),
        )
        
    async def get_room_history(self, room_id: str) -> List[WSMessage]:
        b_messages = await self.redis.lrange(
            name=f"room:{room_id}:messages",
            start=0,
            end=-1,
        )
        return [WSMessage.parse_raw(message.decode()) for message in b_messages]

    async def broadcast(
            self, 
            message: str, 
            room_id: str, 
            sender_id: int,
            is_system: bool = False,
    ) -> None:
        if await self.redis.exists(f"room:{room_id}"):
            users = {member.decode() for member in await self.redis.smembers(f"room:{room_id}")}
            for user_id, connection in self.active_connections.items():
                if str(user_id) in users:
                    message_class = WSMessage(
                        text=message,
                        is_system=is_system,
                        sender_id=int(user_id),
                    )
                    message_dict = message_class.model_dump()
                    message_dict["is_self"] = user_id == sender_id
                    await connection.send_json(message_dict)

manager = ConnectionManager()
