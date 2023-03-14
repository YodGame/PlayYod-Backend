import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse

from settings import JWT_SECRET_KEY, JWT_ALGORITHM
from models.schemas import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class UserSchema(BaseModel):
    username: str
    email: str
    full_name: str


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user_obj = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return JSONResponse(content={"message": "Incorrect username or password"}, status_code=401)

    user_db = await User.query(User.username == user_obj["username"]).all()

    if len(user_db) == 0:
        return JSONResponse(content={"message": "Could not find user"}, status_code=404)
    user_db = user_db[0]

    user = UserSchema(username=user_db.username, email=user_db.email, full_name=user_db.full_name)
    return user
