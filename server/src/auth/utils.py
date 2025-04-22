import datetime
import jwt

from fastapi import Cookie, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.src.security.jwt import decode_token, create_access_token
from server.src.auth.service import get_user
from server.src.auth import exceptions
from server.src.config import settings


async def verify_access_token(
        token: str = Cookie(
            default=None,
            alias=settings.JWT_ACCESS_TOKEN_COOKIE_NAME,
        )
) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
        )
    try:
        return decode_token(token)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )
    

async def refresh_access_token(
        db: AsyncSession,
        refresh_token: str,
) -> str:
    try:
        payload: dict = decode_token(refresh_token)
        user = await get_user(user_id=int(payload.get("sub")), db=db)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired, please re-login"
        )
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    except exceptions.UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User deactivated",
        )
    now = datetime.datetime.now(datetime.UTC)
    new_access_token = create_access_token(
        user_id=user.id,
        now=now,
        payload={
            settings.JWT_TOKEN_PAYLOAD_EMAIL_KEY: user.email,
            settings.JWT_TOKEN_PAYLOAD_ROLE_KEY: user.role,
        },
    )
    return new_access_token