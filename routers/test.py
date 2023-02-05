from fastapi import APIRouter
from models.schemas import TestSchema

router = APIRouter()


# https://aminalaee.dev/mongox/
@router.get('/')
async def root():
    test = await TestSchema.query({"text2": 1}).get()
    print(test)
    return test


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
