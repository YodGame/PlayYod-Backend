from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import test, geo, games
from settings import CLIENT_ORIGINS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CLIENT_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test.router, tags=['Test'], prefix='/test')
app.include_router(geo.router, tags=['Geo'], prefix='/geo')
app.include_router(games.router, tags=['Games'], prefix='/games')
