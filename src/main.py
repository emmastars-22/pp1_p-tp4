from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from models.juego import (
    Juego,
)
from routers.juegos import juegos_routers

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.title = "TP 4"

app.include_router(juegos_routers, tags=["Juegos"], prefix="/juegos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)