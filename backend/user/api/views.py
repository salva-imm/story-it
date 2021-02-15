from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint

from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from user.models import User


class UserRegister(HTTPEndpoint):
    async def post(self, request):
        user_obj = {"username": "mehdi", "email": "mehdi73ee@gmail.com", "is_active": True}
        User_Pydantic = pydantic_model_creator(User)
        print(User_Pydantic(**user_obj))
        return JSONResponse({"data": f"Hello, world!"})
