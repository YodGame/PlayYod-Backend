import json
import urllib.request
import datetime

from bs4 import BeautifulSoup
from models.schemas import TopRecord, TopSeller, Rating


async def top_records():
    now = datetime.datetime.now()

    # Check if current time data not exist in database.
    count = await TopRecord.query({'year': now.year, 'month': now.month, 'day': now.day, 'hour': now.hour}).count()
    if count == 0:
        data = urllib.request.urlopen("https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1")
        data = json.loads(data.read())

        for game in data['response']['ranks']:
            top_records_model = TopRecord(app_id=game['appid'], players=game['concurrent_in_game'], peak_players=game['peak_in_game'], year=now.year, month=now.month, day=now.day, hour=now.hour)
            await top_records_model.insert()

        print(f"Top Records: Fetch SteamChart at {now}")


async def top_sellers():
    now = datetime.datetime.now()

    # Check if current date data not exist in database.
    count = await TopSeller.query({'year': now.year, 'month': now.month, 'day': now.day}).count()
    if count == 0:
        html_data = urllib.request.urlopen("https://store.steampowered.com/search/results?ignore_preferences=1&force_infinite=1&supportedlang=english&filter=globaltopsellers&ndl=1&count=100")
        soup = BeautifulSoup(html_data, 'html.parser')
        lists = soup.select('.search_result_row')
        for game in lists:
            app_id = game.get('data-ds-appid')
            top_sellers_model = TopSeller(app_id=app_id, year=now.year, month=now.month, day=now.day)
            await top_sellers_model.insert()

        print(f"Top Sellers: Fetch Steam Store at {now}")


async def top_ratings():
    now = datetime.datetime.now()

    ratings = await Rating.query().all()
    for game in ratings:
        data = urllib.request.urlopen(
            f"https://store.steampowered.com/appreviews/{game.app_id}?json=1&purchase_type=all&num_per_page=0&language=all")
        data = json.loads(data.read())

        game.review = data["query_summary"]["review_score_desc"]
        game.positive = data["query_summary"]["total_positive"]
        game.negative = data["query_summary"]["total_negative"]
        game.all = data["query_summary"]["total_reviews"]
        await game.save()

    print(f"Top Ratings: Fetch Steam Reviews at {now}")
