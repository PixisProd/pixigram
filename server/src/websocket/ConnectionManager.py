from typing import Dict
import json

from fastapi import WebSocket
import redis.asyncio as redis

from server.src.redis import get_redis_client


class ConnectionManager():
    def __init__(self):
        self.redis: redis.Redis = get_redis_client()
        self.active_connections: Dict[int, WebSocket] = {}
        

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        await self.redis.sadd(room_id, user_id)
    
    
    async def disconnect(self, room_id: int, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        await self.redis.srem(room_id, user_id)
        if await self.redis.scard(room_id) == 0:
            await self.redis.delete(room_id)

    async def save_message(
            self,
            message: str,
            room_id: int, 
            sender_id: int,
            is_system: bool = False,
    ):
        message_class = {
            "text": message,
            "is_system": is_system,
            "sender_id": sender_id,
        }
        await self.redis.lpush(
            f"room:{room_id}:messages", 
            json.dumps(message_class),
        )
        
    async def get_room_history(self, room_id: int):
        b_messages = await self.redis.lrange(
            name=f"room:{room_id}:messages",
            start=0,
            end=-1,
        )
        return [json.loads(message.decode()) for message in b_messages]

    async def broadcast(
            self, 
            message: str, 
            room_id: int, 
            sender_id: int,
            is_system: bool = False,
    ):
        if await self.redis.exists(room_id):
            users = {member.decode() for member in await self.redis.smembers(room_id)}
            for user_id, connection in self.active_connections.items():
                if str(user_id) in users:
                    message_class = {
                        "text": message,
                        "is_self": user_id == sender_id,
                        "is_system": is_system,
                    }
                    await connection.send_json(message_class)

manager = ConnectionManager()
