import datetime

from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from server.src.auth.schemas import RegisterUser
from server.src.auth.service import register_user, login_user, get_user
from server.src.auth import exceptions
from server.src.auth.dependencies import user_dependency
from server.src.auth.utils import refresh_access_token
from server.src.database import db_dependency
from server.src.config import settings
from server.src.security.jwt import (
    create_access_token,
    create_refresh_token,
)


router = APIRouter(
    tags=["Auth 🔓"],
    prefix="/auth",
)


@router.get("/about")
async def about(user: user_dependency, db: db_dependency):
    try:
        return await get_user(user_id=int(user.get("sub")), db=db)
    except exceptions.UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def registration(new_user: RegisterUser, db: db_dependency):
    try:
        await register_user(
            login=new_user.login,
            password=new_user.password,
            username=new_user.username,
            email=new_user.email,
            db=db,
        )
        return JSONResponse(
            content={"msg": "User successfully registered"},
            status_code=status.HTTP_201_CREATED,
        )
    except exceptions.UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    db: db_dependency,
    credentials: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
):
    try:
        user = await login_user(
            login=credentials.username,
            password=credentials.password,
            db=db,
        )
        now = datetime.datetime.now(datetime.UTC)
        access_token = create_access_token(
            user_id=user.id,
            now=now,
            payload={
                settings.JWT_TOKEN_PAYLOAD_EMAIL_KEY: user.email,
                settings.JWT_TOKEN_PAYLOAD_ROLE_KEY: user.role,
            },
        )
        refresh_token = create_refresh_token(
            user_id=user.id,
            now=now,
        )
        response = JSONResponse(content={"msg": "Successful login"})
        response.set_cookie(
            key=settings.JWT_ACCESS_TOKEN_COOKIE_NAME,
            value=access_token,
        )
        response.set_cookie(
            key=settings.JWT_REFRESH_TOKEN_COOKIE_NAME,
            value=refresh_token,
        )
        return response
    except exceptions.IncorrectCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except exceptions.DeactivatedUserException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    

@router.post("/refresh-token")
async def refresh_token(
    db: db_dependency,
    refresh_token: str = Cookie(
        default=None,
        alias=settings.JWT_REFRESH_TOKEN_COOKIE_NAME,
    )
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token missing",
        )
    new_access_token = await refresh_access_token(
        db=db,
        refresh_token=refresh_token,
    )
    response = JSONResponse(
        content={"msg": "Token successfully refreshed"},
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key=settings.JWT_ACCESS_TOKEN_COOKIE_NAME,
        value=new_access_token,
    )
    return response
