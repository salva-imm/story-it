from datetime import datetime
from utils.base import BaseOrmModelSerializer


class UsersSerializer(BaseOrmModelSerializer):
    id: int
    username: str
    email: str
    join_date: datetime
