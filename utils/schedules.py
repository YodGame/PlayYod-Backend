import json
import urllib.request
import datetime
from models.schemas import TopRecord


async def top_records():
    now = datetime.datetime.now()

    # Check if current time data not exist in database.
    count = await TopRecord.query({'year': now.year, 'month': now.month, 'day': now.day, 'hour': now.hour}).count()
    if count == 0:
        data = urllib.request.urlopen(f"https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1")
        data = json.loads(data.read())

        for game in data['response']['ranks']:
            top_records_model = TopRecord(app_id=game['appid'], players=game['concurrent_in_game'], peak_players=game['peak_in_game'], year=now.year, month=now.month, day=now.day, hour=now.hour)
            await top_records_model.insert()

        print(f"Top Records: Fetch SteamChart at {now}")


