import datetime
from typing import Union

from fastapi import APIRouter
from mongox import Q

from models.schemas import Game, TopSeller
from utils.motor_q import aggregate

router = APIRouter()


@router.get('/records')
async def top_records(date: Union[str, None] = None, previous_days: Union[int, None] = None, limit=50):
    records = []

    pipeline = [
        {"$group": {
            "_id": "$app_id",
            "max_players": {"$max": "$players"}
        }},
        {"$lookup": {
            "from": "top_records",
            "let": {"app_id": "$_id", "max_players": "$max_players"},
            "pipeline": [
                {"$match": {"$expr": {"$and": [
                    {"$eq": ["$app_id", "$$app_id"]},
                    {"$eq": ["$players", "$$max_players"]}
                ]}}},
                {"$project": {
                    "year": 1,
                    "month": 1,
                    "day": 1,
                    "hour": 1
                }}
            ],
            "as": "player_doc"
        }},
        {"$unwind": "$player_doc"},
        {"$sort": {"max_players": -1}},
        {"$limit": limit},
        {"$project": {
            "_id": 0,
            "app_id": "$_id",
            "players": "$max_players",
            "year": "$player_doc.year",
            "month": "$player_doc.month",
            "day": "$player_doc.day",
            "hour": "$player_doc.hour"
        }}
    ]

    try:
        if date is not None:
            date_object = datetime.datetime.strptime(date, '%Y-%m-%d')
            pipeline.insert(0, {"$match": {
                "year": date_object.year,
                "month": date_object.month
            }})
        if previous_days is not None:
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=previous_days)
            pipeline.insert(0, {
                "$match": {
                    "year": {"$gte": start_date.year},
                    "month": {"$gte": start_date.month},
                    "day": {"$gte": start_date.day},
                    "$and": [
                        {"year": {"$lte": end_date.year}},
                        {"month": {"$lte": end_date.month}},
                        {"day": {"$lte": end_date.day}}
                    ]
                }
            })

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


@router.get('/records/today')
async def top_records_today(limit=20):
    records = []
    date_object = datetime.datetime.now()

    pipeline = [
        {"$match": {
            "year": date_object.year,
            "month": date_object.month,
            "day": date_object.day
        }},
        {"$group": {
            "_id": "$app_id",
            "players": {"$max": "$players"}
        }},
        {"$sort": {"players": -1}},
        {"$limit": limit},
        {"$project": {
            "_id": 0,
            "app_id": "$_id",
            "players": 1
        }}
    ]

    data = await aggregate('top_records', pipeline)
    start_date = date_object - datetime.timedelta(days=7)

    game_list = [d['app_id'] for d in data]
    game_name_list = await Game.query(Q.in_(Game.app_id, game_list)).all()

    for i in range(0, len(data)):
        pipeline = [
            {
                "$match": {
                    "app_id": data[i]['app_id'],
                    "year": {"$gte": start_date.year},
                    "month": {"$gte": start_date.month},
                    "day": {"$gte": start_date.day},
                    "$and": [
                        {"year": {"$lte": date_object.year}},
                        {"month": {"$lte": date_object.month}},
                        {"day": {"$lte": date_object.day}}
                    ]
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": "$year",
                        "month": "$month",
                        "day": "$day"
                    },
                    "peak_players": {"$max": "$peak_players"}
                }
            },
            {
                "$sort": {"_id.year": -1, "_id.month": -1, "_id.day": -1}
            }
        ]
        previous = await aggregate('top_records', pipeline)
        previous_list = []
        for p in previous:
            dt = datetime.datetime(year=p['_id']['year'], month=p['_id']['month'], day=p['_id']['day'])
            previous_list.append({'players': p['peak_players'], 'timestamp': int(dt.timestamp())})

        game_name_index = next((index for (index, d) in enumerate(game_name_list) if d.app_id == data[i]['app_id']),
                               None)

        records.append({'name': game_name_list[game_name_index].name if game_name_index is not None else '',
                        'players': data[i]['players'], 'previous': previous_list})

    return records


@router.get('/sellers')
async def top_sellers(date: Union[str, None] = None, limit=50):
    sellers = []
    date_object = datetime.datetime.now()

    try:
        if date is not None:
            date_object = datetime.datetime.strptime(date, '%Y-%m-%d')
    except:
        pass

    data = await TopSeller.query({'year': date_object.year, 'month': date_object.month, 'day': date_object.day}).limit(
        limit).all()
    game_list = [d.app_id for d in data]

    game_name_list = await Game.query(Q.in_(Game.app_id, game_list)).all()

    for game in data:
        game_name_index = next((index for (index, d) in enumerate(game_name_list) if d.app_id == game.app_id),
                               None)
        sellers.append({'app_id': game.app_id,
                        'name': game_name_list[game_name_index].name if game_name_index is not None else ''})

    return sellers
