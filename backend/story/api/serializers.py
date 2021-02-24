from utils.base import BaseOrmModelSerializer


class StoriesSerializer(BaseOrmModelSerializer):
    id: int
    title: str
    content: str
    draft: bool
