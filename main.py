import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import test, geo, games, top
from settings import CLIENT_ORIGINS
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.schedules import top_records, top_sellers

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
app.include_router(top.router, tags=['Top'], prefix='/top')


@app.on_event('startup')
def init_data():
    scheduler = AsyncIOScheduler()
    # years, months, days, hours, minutes, seconds
    scheduler.add_job(top_records, 'interval', hours=1, next_run_time=datetime.datetime.now())
    scheduler.add_job(top_sellers, 'interval', days=1, next_run_time=datetime.datetime.now())
    scheduler.start()
