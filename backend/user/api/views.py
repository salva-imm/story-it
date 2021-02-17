from pydantic import BaseModel, constr
from starlette.responses import JSONResponse

from user.models import User

from utils.base import BaseEndpoint


class UserRegister(BaseEndpoint):
    class Arguments(BaseModel):
        username: constr(max_length=2)
        password: constr(max_length=128)
        email: constr(max_length=128)

    class Validator:
        def validate_username(self):
            # TODO: check username uniqueness
            pass

        def validate_email(self):
            # TODO: check email uniqueness
            pass

    async def post(self, request):
        data = await request.json()
        self.is_valid(**data)
        return JSONResponse({"data": f"Hello, world!"})
