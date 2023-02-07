import json
import urllib.parse
import urllib.request

from fastapi import APIRouter

router = APIRouter()


@router.get('/search/{app}')
async def search(app: str):
    data = urllib.request.urlopen(f"https://steamcommunity.com/actions/SearchApps/{urllib.parse.quote(app)}")
    data = json.loads(data.read())

    for d in data:
        del d['icon']
        del d['logo']

    return data
