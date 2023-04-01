import json
import urllib.request
from typing import Union

from fastapi import APIRouter

router = APIRouter()


@router.get('/search')
async def search(keyword: Union[str, None] = None):
    search = []

    if keyword:
        headers = {'User-Agent': 'PlayYod/1.0'}
        req = urllib.request.Request(f"https://www.reddit.com/search.json?q={keyword}&sort=hot&limit=15&type=link&show=posts", headers=headers)
        data = urllib.request.urlopen(req)
        data = json.loads(data.read())

        for item in data["data"]["children"]:
            url = item["data"]["permalink"]
            thumbnail = item["data"]["thumbnail"] if str(item["data"]["thumbnail"]).startswith("https://") else None

            search.append({
                "title": item["data"]["title"],
                "author": item["data"]["author"],
                "subreddit": item["data"]["subreddit_name_prefixed"],
                "ups": item["data"]["ups"],
                "num_comments": item["data"]["num_comments"],
                "flair_name": item["data"]["link_flair_text"],
                "flair_color": item["data"]["link_flair_background_color"],
                "thumbnail": thumbnail,
                "url": f"https://www.reddit.com{url}"
            })

    return search
