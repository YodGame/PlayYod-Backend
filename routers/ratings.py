from fastapi import APIRouter, Query
from mongox import Q

from models.schemas import Rating, Game

router = APIRouter()


@router.get('/top')
async def top(limit: int = Query(default=50, ge=0, le=100, description="")):
    ratings = []

    data = await Rating.query().limit(limit).all()
    game_list = [d.app_id for d in data]

    game_name_list = await Game.query(Q.in_(Game.app_id, game_list)).all()
    for game in data:
        game_name_index = next((index for (index, d) in enumerate(game_name_list) if d.app_id == game.app_id),
                               None)
        ratings.append({
            'app_id': game.app_id,
            'name': game_name_list[game_name_index].name if game_name_index is not None else '',
            'review': game.review,
            'positive': game.positive,
            'negative': game.negative,
            'all': game.all
        })

    return ratings
