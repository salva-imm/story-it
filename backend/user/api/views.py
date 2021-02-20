from user.models import User
from pydantic import BaseModel, constr

from utils.base import BaseEndpoint
from starlette.responses import JSONResponse

from .serializers import UsersSerializer

from argon2 import PasswordHasher


class UserRegister(BaseEndpoint):
    class Arguments(BaseModel):
        username: constr(max_length=128)
        password: constr(max_length=128)
        email: constr(max_length=128)

    @classmethod
    async def validate_username(cls, username):
        await cls.check_unique(User, username=username)

    @classmethod
    async def validate_email(cls, email):
        await cls.check_unique(User, email=email)

    async def post(self, request):
        data = await request.json()
        await self.is_valid(**data)
        ph = PasswordHasher()
        data['password'] = ph.hash(data.get('data'))
        user = await User.create(**data)
        res = UsersSerializer.get_response(user)
        return JSONResponse({"data": res})
