from datetime import datetime
from utils.base import BaseOrmModelSerializer


class CommentsSerializer(BaseOrmModelSerializer):
    id: int
    user_id: int
    story_id: int
    content: str
    date: datetime
