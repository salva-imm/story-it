import json
from pydantic import BaseModel
from argon2 import PasswordHasher
from tortoise.exceptions import DoesNotExist
from pydantic.error_wrappers import ValidationError
from starlette.endpoints import HTTPEndpoint, HTTPException


class BaseEndpoint(HTTPEndpoint):
    class Arguments:
        def __init__(self, **data):
            pass

    async def is_valid(self, **data):
        try:
            self.Arguments(**data)
        except ValidationError as v:
            raise HTTPException(detail=v.json(), status_code=400)

        this = self.scope['endpoint']
        for item in vars(this):
            if 'validate' in item:
                arg = getattr(this, item).__code__.co_varnames[1]
                await getattr(this, item)(data.get(arg))

    @classmethod
    async def check_unique(cls, model, **kwargs):
        try:
            await model.get(**kwargs)
            raise HTTPException(detail=f"{next(iter(kwargs.keys()))} already exist!", status_code=400)
        except DoesNotExist:
            pass


class BaseOrmModelSerializer(BaseModel):
    class Config:
        orm_mode = True

    @classmethod
    def get_response(cls, model):
        return json.loads(cls.from_orm(model).json())


password_hasher = PasswordHasher()
