from fastapi import APIRouter, HTTPException, status

from server.src.auth.schemas import RegisterUser
from server.src.auth.service import register_user
from server.src.auth.exceptions import UserAlreadyExistsException
from server.src.database import db_dependency


router = APIRouter(
    tags=["Auth 🔓"],
    prefix="/auth"
)


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def registration(new_user: RegisterUser, db: db_dependency):
    try:
        await register_user(
            login=new_user.login,
            password=new_user.password,
            username=new_user.username,
            email=new_user.email,
            db=db
        )
        return {"msg": "User successfully registered"}
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

