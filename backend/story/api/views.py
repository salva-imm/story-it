from story.models import Story
from pydantic import BaseModel, constr
from utils.base import BaseEndpoint, base_auth

from .serializers import StoriesSerializer
from starlette.responses import JSONResponse


class CreateStory(BaseEndpoint):
    class Arguments(BaseModel):
        title: constr(max_length=128, min_length=3)
        content: constr(min_length=3)
        draft: bool

    @base_auth.login_required
    @base_auth.is_owner('Story', 'body')
    async def post(self, request):
        data = await request.json()
        await self.is_valid(**data)
        data['user_id'] = request.payload.get('user_id')
        story = await Story.create(**data)
        res = StoriesSerializer.get_response(story)
        return JSONResponse({"data": res})


class DeleteStory(BaseEndpoint):

    @base_auth.login_required
    @base_auth.is_owner('Story', 'body')
    async def delete(self, request):
        data = await request.json()
        await self.is_valid(**data)
        data['user_id'] = request.payload.get('user_id')
        story = await Story.create(**data)
        res = StoriesSerializer.get_response(story)
        return JSONResponse({"data": res})
