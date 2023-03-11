import json
import urllib.request

from fastapi import APIRouter
from mongox import Q
from models.schemas import Country

router = APIRouter()


@router.get('/players')
async def players():
    players = []
    # example data
    countries = await Country.query(
        Q.in_(Country.alpha_2, ['US', 'CN', 'RU', 'BR', 'DE', 'CA', 'FR', 'GB', 'PL', 'TR'])).all()

    test_num = 15000
    for country in countries:
        players.append({'name': country.alpha_2, 'users': test_num})
        test_num -= 1000

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
