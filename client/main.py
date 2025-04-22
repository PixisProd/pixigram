from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from client.front.router import router as front_router


app = FastAPI(
    title="pixigram"
)


app.mount("/client/static", StaticFiles(directory="client/static"), name="static")


app.include_router(front_router)