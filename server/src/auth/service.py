import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from server.src.auth import exceptions
from server.src.security.bcrypt import bcrypt_context
from server.src.models import OrmUser
from server.src.config import settings


async def get_user(user_id: int, db: AsyncSession):
    query = select(OrmUser).where(OrmUser.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise exceptions.UserNotFoundException()
    return user


async def register_user(
        login: str, password: str, username: str, email: str, db: AsyncSession
) -> None:
    hashed_password = bcrypt_context.hash(password)
    db.add(OrmUser(
        login=login,
        password=hashed_password,
        username=username,
        email=email,
    ))
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise exceptions.UserAlreadyExistsException()
    

async def login_user(
        login: str, password: str, db: AsyncSession
) -> OrmUser:
    query = select(OrmUser).where(OrmUser.login == login)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user or not bcrypt_context.verify(password, user.password):
        raise exceptions.IncorrectCredentialsException()
    if not user.is_active:
        raise exceptions.DeactivatedUserException()
    return user


