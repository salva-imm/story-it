from init_db import db_arguments
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
import base64
import binascii

from tortoise.contrib.starlette import register_tortoise

from user.api.urls import routes as user_routes
from story.api.urls import routes as story_routes


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        # TODO: You'd want to verify the username and password here.
        return AuthCredentials(["authenticated"]), SimpleUser(username)


async def home(request):
    if request.user.is_authenticated:
        return JSONResponse({'data': request.user.display_name})
    return JSONResponse({"data": "Hello,World"})


middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

routes = [
    Route('/', home),
]

routes.extend(user_routes)
routes.extend(story_routes)

app = Starlette(debug=True, routes=routes, middleware=middleware)

register_tortoise(
    app, generate_schemas=False, **db_arguments
)
