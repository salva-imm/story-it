from user.models import User
from pydantic import BaseModel, constr
from tortoise.exceptions import DoesNotExist

from utils.base import BaseEndpoint
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPException

from .serializers import UsersSerializer


class UserRegister(BaseEndpoint):
    class Arguments(BaseModel):
        username: constr(max_length=128)
        password: constr(max_length=128)
        email: constr(max_length=128)

    class Validator:
        async def validate_username(self, username):
            try:
                await User.get(username=username.lower())
                raise HTTPException(detail="Username already exist!", status_code=400)
            except DoesNotExist:
                pass

        async def validate_email(self, email):
            try:
                await User.get(email=email.lower())
                raise HTTPException(detail="Email already exist!", status_code=400)
            except DoesNotExist:
                pass

    async def post(self, request):
        data = await request.json()
        await self.is_valid(**data)
        user = await User.create(**data)
        res = UsersSerializer.get_response(user)
        return JSONResponse({"data": res})
