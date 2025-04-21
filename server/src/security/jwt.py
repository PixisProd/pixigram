import datetime
from typing import Any

import jwt

from server.src.config import settings


def create_token(
        user_id: int, 
        now: datetime.datetime, 
        lifetime: datetime.timedelta,
        payload: dict[str, Any] | None = None,
) -> str:
    temp_payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + lifetime
    }
    if payload:
        temp_payload.update(payload)
    return jwt.encode(
        payload=temp_payload,
        key=settings.JWT_TOKEN_SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_TOKEN_ALGORITHM,
    )


def create_access_token(
        user_id: int,
        now: datetime.datetime,
        payload: dict[str, Any],
) -> str:
    return create_token(
        user_id=user_id,
        now=now,
        lifetime=settings.JWT_ACCESS_TOKEN_LIFETIME,
        payload=payload,
    )


def create_refresh_token(
        user_id: int,
        now: datetime.datetime,
) -> str:
    return create_token(
        user_id=user_id,
        now=now,
        lifetime=settings.JWT_REFRESH_TOKEN_LIFETIME,
    )


def decode_token(token: str) -> dict:
    return jwt.decode(
        jwt=token,
        key=settings.JWT_TOKEN_SECRET_KEY.get_secret_value(),
        algorithms=settings.JWT_TOKEN_ALGORITHM,
    )