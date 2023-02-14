import motor.motor_asyncio
from settings import MONGODB_URI, MONGODB_COLLECTION

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_COLLECTION]


async def aggregate(collection: str, pipeline: list):
    collection = db[collection]
    cursor = collection.aggregate(pipeline)

    data = []
    async for doc in cursor:
        data.append(doc)

    return data


async def find(collection: str, find_dict: dict, sort_list: list = None):
    collection = db[collection]

    if sort_list:
        cursor = collection.find(find_dict).sort(sort_list)
    else:
        cursor = collection.find(find_dict)

    data = []
    async for doc in cursor:
        data.append(doc)

    return data

