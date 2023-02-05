from settings import MONGODB_URI, MONGODB_COLLECTION

import mongox

client = mongox.Client(MONGODB_URI)
db = client.get_database(MONGODB_COLLECTION)


class TestSchema(mongox.Model, db=db):
    text1: str
    text2: int
