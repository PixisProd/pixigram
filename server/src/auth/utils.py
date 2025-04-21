import jwt

from fastapi import Cookie, HTTPException, status

from server.src.security.jwt import decode_token
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