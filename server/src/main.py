from fastapi import FastAPI
from contextlib import asynccontextmanager

from server.src.database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="pixigram",
    lifespan=lifespan
)


