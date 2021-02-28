from comment.models import Comment
from pydantic import BaseModel, constr, conint
from utils.base import BaseEndpoint, base_auth

from .serializers import CommentsSerializer
from starlette.responses import JSONResponse


class CreateComment(BaseEndpoint):
    class Arguments(BaseModel):
        content: constr(min_length=3)
        story_id: conint(gt=0)

    @base_auth.login_required
    async def post(self, request):
        data = await request.json()
        await self.is_valid(**data)
        data['user_id'] = request.payload.get('user_id')
        comment = await Comment.create(**data)
        res = CommentsSerializer.get_response(comment)
        return JSONResponse({"data": res})
