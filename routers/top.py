import datetime
from typing import Union

from fastapi import APIRouter
from mongox import Q

from models.schemas import Game, TopSeller
from utils.motor_q import aggregate

router = APIRouter()


@router.get('/records')
async def top_records(date: Union[str, None] = None):
    records = []

    pipeline = [
        {"$group": {
            "_id": "$app_id",
            "players": {"$max": "$players"},
            "year": {"$first": "$year"},
            "month": {"$first": "$month"},
            "day": {"$first": "$day"},
            "hour": {"$first": "$hour"}
        }},
        {"$sort": {"players": -1}},
        {"$limit": 50},
        {"$project": {
            "_id": 0,
            "app_id": "$_id",
            "players": 1,
            "year": 1,
            "month": 1,
            "day": 1,
            "hour": 1
        }}
    ]

    try:
        if date is not None:
            date_object = datetime.datetime.strptime(date, '%Y-%m-%d')
            pipeline.append({"$match": {
                "year": date_object.year,
                "month": date_object.month
            }})
    except:
        pass

    data = await aggregate('top_records', pipeline)
    game_list = [d['app_id'] for d in data]

    game_name_list = await Game.query(Q.in_(Game.app_id, game_list)).all()

    for i in range(0, len(data)):
        game_name_index = next((index for (index, d) in enumerate(game_name_list) if d.app_id == data[i]['app_id']),
                               None)
        dt = datetime.datetime(year=data[i]['year'], month=data[i]['month'], day=data[i]['day'], hour=data[i]['hour'])

        records.append({'name': game_name_list[game_name_index].name if game_name_index is not None else '',
                        'players': data[i]['players'], 'time': int(dt.timestamp())})

    return records


@router.get('/sellers')
async def top_records(date: Union[str, None] = None):
    sellers = []
    date_object = datetime.datetime.now()

    try:
        if date is not None:
            date_object = datetime.datetime.strptime(date, '%Y-%m-%d')
    except:
        pass

    data = await TopSeller.query({'year': date_object.year, 'month': date_object.month, 'day': date_object.day}).limit(50).all()
    game_list = [d.app_id for d in data]

    game_name_list = await Game.query(Q.in_(Game.app_id, game_list)).all()

    for game in data:
        game_name_index = next((index for (index, d) in enumerate(game_name_list) if d.app_id == game.app_id),
                               None)
        sellers.append({'app_id': game.app_id, 'name': game_name_list[game_name_index].name if game_name_index is not None else ''})

    return sellers
