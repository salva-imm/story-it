from story.models import Story
from pydantic import BaseModel, constr
from utils.base import BaseEndpoint

from .serializers import StoriesSerializer
from starlette.responses import JSONResponse


class CreateStory(BaseEndpoint):
    class Arguments(BaseModel):
        title: constr(max_length=128, min_length=3)
        content: constr(min_length=3)
        draft: bool

    async def post(self, request):
        data = await request.json()
        await self.is_valid(**data)
        story = await Story.create(**data)
        res = StoriesSerializer.get_response(story)
        return JSONResponse({"data": res})
