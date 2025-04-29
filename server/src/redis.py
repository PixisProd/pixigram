from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends


redis_pool = redis.ConnectionPool.from_url("redis://localhost")
redis_client = redis.Redis.from_pool(redis_pool)


async def get_redis_client() -> redis.Redis:
    return redis_client


redis_dependency = Annotated[redis.Redis, Depends(get_redis_client)]