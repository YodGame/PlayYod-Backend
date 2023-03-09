from fastapi import APIRouter

from routers.top import top_sellers, top_records, top_records_today

router = APIRouter()


@router.get('/summary')
async def summary():
    summary = {}

    t_sellers = await top_sellers(limit=10)
    t_records = await top_records(limit=10)
    t_players_7_days = await top_records(previous_days=7, limit=10)
    players_today = await top_records_today(limit=10)

    summary['top_sellers'] = t_sellers
    summary['top_records'] = t_records
    summary['top_players_7_days'] = t_players_7_days
    summary['players_today'] = players_today

    return summary
