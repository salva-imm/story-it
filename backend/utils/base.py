import os
import json
from jose import jwt, exceptions
from pydantic import BaseModel
from argon2 import PasswordHasher
from functools import wraps
from datetime import datetime, timedelta
from tortoise.exceptions import DoesNotExist
from pydantic.error_wrappers import ValidationError
from starlette.endpoints import HTTPEndpoint, HTTPException


SECRET_KEY = os.getenv(
    "STORY_APP_SECRET_KEY",
    "test_09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1


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


class BaseAuth:
    def __init__(self, secret, algorithms, expire_days):
        self.secret = secret
        self.algorithms = algorithms
        self.expire_days = expire_days

    async def check_auth_header(self, request):
        try:
            info = jwt.decode(request.headers.get("Authorization"), self.secret, algorithms=[self.algorithms])
            expire_date = datetime.strptime(info['payload']['expire_date'], '%m/%d/%Y, %H:%M:%S')
            if expire_date < datetime.now():
                raise exceptions.JWTError
        except exceptions.JWTError:
            raise HTTPException(detail="The token is not valid!", status_code=401)
        return info

    def login_required(self, func):
        @wraps(func)
        async def check_auth_header(*args, **kwargs):
            request = args[1]
            info = await self.check_auth_header(request)
            args[1].payload = info.get('payload')
            value = await func(*args, **kwargs)
            return value
        return check_auth_header

    def create_token(self, user):
        expire_date = datetime.now() + timedelta(days=self.expire_days)
        payload = {
            "user_id": user.id,
            "username": user.username,
            "expire_date": expire_date.strftime("%m/%d/%Y, %H:%M:%S")
        }
        token = jwt.encode({'payload': payload}, self.secret, algorithm=self.algorithms)
        return token

    def is_owner(self, model, id_place):
        # id_place could be `headers`, `path_params` and maybe `query_params` in some cases!!
        def inner(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                request = args[1]
                info = request.get('payload')
                if not info:
                    # scream!!
                    print('hell!')
                    info = self.check_auth_header(request).get('payload')

                final_id = request.get(id_place).get('id')
                try:
                    await model.get(id=final_id, user_id=info.get('user_id'))
                except DoesNotExist:
                    raise HTTPException(detail=f"You're not owner of this {model.__name__}!", status_code=403)

                await func(*args, **kwargs)

            return wrapper

        return inner


base_auth = BaseAuth(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS)
