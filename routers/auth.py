from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, constr
from models.schemas import User
from mongox import Q
from settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_TOKEN_EXPIRE_MINUTES

import jwt
import utils.oauth
import datetime

router = APIRouter()


class RegisterForm(BaseModel):
    username: constr(min_length=3, max_length=20)
    email: EmailStr
    password: str
    full_name: constr(max_length=100)


class LoginForm(BaseModel):
    username: str
    password: str


@router.post('/register')
async def register(form_data: RegisterForm = Form()):
    username = form_data.username.lower()
    email = form_data.email.lower()

    check = await User.query(Q.or_(User.username == username, User.email == email)).count()
    if check != 0:
        return {
            "status": "error",
            "message": "Username or email already exists."
        }

    user = await User(username=username, email=email, full_name=form_data.full_name, password=utils.oauth.get_hashed_password(form_data.password)).insert()
    if user:
        return {
            "status": "success",
            "message": ""
        }

    return {}


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username.lower()

    user = await User.query(Q.or_(User.username == username, User.email == username)).all()
    if len(user) == 0:
        return {
            "status": "error",
            "message": "Username or email does not exist."
        }

    user = user[0]

    if utils.oauth.verify_password(form_data.password, user.password):
        token = jwt.encode({
            "username": user.username,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=JWT_TOKEN_EXPIRE_MINUTES)
        }, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    else:
        return {
            "status": "error",
            "message": "Password is incorrect."
        }


@router.get('/me')
async def me(user: utils.oauth.UserSchema = Depends(utils.oauth.get_current_user)):
    return user
