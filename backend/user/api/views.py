import os
from datetime import datetime, timedelta

from user.models import User
from jose import jwt
from pydantic import BaseModel, constr
from tortoise.query_utils import Q
from tortoise.exceptions import DoesNotExist

from starlette.responses import JSONResponse
from starlette.endpoints import HTTPException

from utils.base import BaseEndpoint, password_hasher
from argon2 import exceptions
from .serializers import UsersSerializer

SECRET_KEY = os.getenv(
    "STORY_APP_SECRET_KEY",
    "test_09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1


class UserRegister(BaseEndpoint):
    class Arguments(BaseModel):
        username: constr(max_length=128, min_length=3)
        password: constr(max_length=128, min_length=8)
        email: constr(max_length=128, min_length=5)

    @classmethod
    async def validate_username(cls, username):
        await cls.check_unique(User, username=username)

    @classmethod
    async def validate_email(cls, email):
        await cls.check_unique(User, email=email)

    async def post(self, request):
        data = await request.json()
        await self.is_valid(**data)
        data['password'] = password_hasher.hash(data.get('password'))
        user = await User.create(**data)
        res = UsersSerializer.get_response(user)
        return JSONResponse({"data": res})


class Auth(BaseEndpoint):
    class Arguments(BaseModel):
        username: constr(max_length=128, min_length=3)
        password: constr(max_length=128, min_length=8)

    async def post(self, request):
        data = await request.json()
        await self.is_valid(**data)
        try:
            user = await User.get(Q(username=data.get('username')) | Q(email=data.get('username')))
        except DoesNotExist:
            raise HTTPException(detail="User or password is not valid!", status_code=400)
        try:
            password_hasher.verify(user.password, data.get('password'))
        except exceptions.VerifyMismatchError:
            raise HTTPException(detail="User or password is not valid!", status_code=400)
        expire_date = datetime.now() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        payload = {
            "user_id": user.id,
            "username": user.username,
            "expire_date": expire_date.strftime("%m/%d/%Y, %H:%M:%S")
        }
        token = jwt.encode({'payload': payload}, SECRET_KEY, algorithm=ALGORITHM)
        return JSONResponse({"data": token})
