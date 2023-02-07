from settings import MONGODB_URI, MONGODB_COLLECTION

import mongox

client = mongox.Client(MONGODB_URI)
db = client.get_database(MONGODB_COLLECTION)


# https://aminalaee.dev/mongox/
class TestSchema(mongox.Model, db=db):
    text1: str
    text2: int


class Country(mongox.Model, db=db, collection="countries"):
    name: str
    alpha_2: str = mongox.Field(..., min_length=2, max_length=2)
    alpha_3: str = mongox.Field(..., min_length=3, max_length=3)
    region: str
