from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(
    tags=["Front 🖼️"]
)


@router.get("/login")
async def read_root():
    return FileResponse("client/static/login.html")


@router.get("/about")
async def about_user():
    return FileResponse("client/static/about.html")


@router.get("/registration")
async def register_user():
    return FileResponse("client/static/registration.html")