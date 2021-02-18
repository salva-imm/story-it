import json
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from starlette.endpoints import HTTPEndpoint, HTTPException


class BaseEndpoint(HTTPEndpoint):
    class Arguments:
        def __init__(self, **data):
            pass

    class Validator:
        pass

    async def is_valid(self, **data):
        try:
            self.Arguments(**data)
        except ValidationError as v:
            raise HTTPException(detail=v.json(), status_code=400)

        val_class = self.Validator()
        for item in vars(self.Validator):
            if 'validate' in item:
                arg = getattr(val_class, item).__code__.co_varnames[1]
                await getattr(val_class, item)(data.get(arg))


class BaseOrmModelSerializer(BaseModel):
    class Config:
        orm_mode = True

    @classmethod
    def get_response(cls, model):
        return json.loads(cls.from_orm(model).json())
