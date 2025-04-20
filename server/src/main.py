from fastapi import FastAPI
from contextlib import asynccontextmanager

from server.src.database import create_tables, delete_tables
from server.src import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(
    title="pixigram",
    lifespan=lifespan,
)


app.include_router(router)
