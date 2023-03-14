from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = token
    return user
