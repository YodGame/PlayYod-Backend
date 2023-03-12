import json
import urllib.request
import pandas as pd

from fastapi import APIRouter
from mongox import Q
from models.schemas import Country

router = APIRouter()


@router.get('/players')
async def players():
    players = []

    json_str = urllib.request.urlopen(
        f"https://cdn.akamai.steamstatic.com/steam/publicstats/download_traffic_per_country.json")
    json_str = json_str.read().decode("utf-8").replace('onTrafficData(', '').replace(');', '')

    df = pd.read_json(json_str, orient='index')

    # Calculate total number of bytes for all countries
    total_bytes = df["totalbytes"].sum()

    # Calculate percentage of total bytes for each country
    df["percentage_bytes"] = df["totalbytes"] / total_bytes * 100

    # Format percentage values
    df["percentage_bytes"] = df["percentage_bytes"].map("{:.3f}".format)

    online_data = urllib.request.urlopen("https://store.steampowered.com/stats/userdata.json?days_back=3")
    online_data = json.loads(online_data.read())[0]['data'][-1][1]

    for i, country in df.iterrows():
        if country["percentage_bytes"] == "0.000":
            continue

        try:
            country_info = await Country.query({'alpha_3': i}).get()
            players.append({'name': country_info.name, 'users': int((online_data * float(country["percentage_bytes"])) / 100)})
        except:
            pass

    return players


@router.get('/game/{app_id}')
async def game(app_id: str):
    players = {}

    data = urllib.request.urlopen(f"https://store.steampowered.com/api/appdetails?appids={app_id}")
    data = json.loads(data.read())

    if not data[app_id]["success"]:
        return players

    players["name"] = data[app_id]["data"]["name"]
    # example data
    countries = await Country.query(
        Q.in_(Country.alpha_2, ['US', 'CN', 'RU', 'BR', 'DE', 'CA', 'FR', 'GB', 'PL', 'TR'])).all()

    test_num = 15000
    country_player = []
    for country in countries:
        country_player.append({'name': country.alpha_2, 'users': test_num})
        test_num -= 1000

    players["players"] = country_player

    return players
