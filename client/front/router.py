from fastapi import APIRouter, status
from fastapi.responses import FileResponse, RedirectResponse


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


@router.get("/chat")
async def chat():
    return FileResponse("client/static/chat.html")


@router.get("/{echo:path}")
async def root():
    return RedirectResponse(
        url="/about",
        status_code=status.HTTP_308_PERMANENT_REDIRECT
    )