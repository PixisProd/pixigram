from fastapi import APIRouter

from server.src.auth.router import router as auth_router
from server.src.websocket.router import router as websocket_router


router = APIRouter()


router.include_router(auth_router)
router.include_router(websocket_router)