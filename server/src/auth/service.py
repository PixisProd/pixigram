from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from server.src.auth.exceptions import UserAlreadyExistsException
from server.src.security.bcrypt import bcrypt_context
from server.src.models import OrmUser


async def register_user(
        login: str, password: str, username: str, email: str, db: AsyncSession
) -> None:
    hashed_password = bcrypt_context.hash(password)
    db.add(OrmUser(
        login=login,
        password=hashed_password,
        username=username,
        email=email
    ))
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise UserAlreadyExistsException()