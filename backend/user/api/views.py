from user.models import User
from pydantic import BaseModel, constr
from tortoise.query_utils import Q
from tortoise.exceptions import DoesNotExist

from starlette.responses import JSONResponse
from starlette.endpoints import HTTPException

from utils.base import BaseEndpoint, password_hasher, base_auth
from argon2 import exceptions
from .serializers import UsersSerializer


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
        token = base_auth.create_token(user)
        return JSONResponse({"data": token})
