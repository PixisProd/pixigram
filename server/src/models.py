import datetime

from enum import StrEnum

from sqlalchemy import Integer, String, Enum, text, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class OrmBase(DeclarativeBase):
    pass


class Roles(StrEnum):
    admin = "admin"
    user = "user"

class OrmUser(OrmBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    login: Mapped[str] = mapped_column(
        String,
        index=True,
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(
        String,
        index=True,
        unique=True,
        nullable=False,
    )
    role: Mapped[Roles] = mapped_column(
        Enum(Roles),
        nullable=False,
        default=Roles.user,
        server_default=text(f"'{Roles.user}'"),
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC),
    )