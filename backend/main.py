from init_db import db_arguments
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from tortoise.contrib.starlette import register_tortoise

from user.api.urls import routes as user_routes
from story.api.urls import routes as story_routes


async def home(request):
    if request.user.is_authenticated:
        return JSONResponse({'data': request.user.display_name})
    return JSONResponse({"data": "Hello,World"})


routes = [
    Route('/', home),
]

routes.extend(user_routes)
routes.extend(story_routes)

app = Starlette(debug=True, routes=routes)

register_tortoise(
    app, generate_schemas=False, **db_arguments
)
