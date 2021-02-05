from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


def home():
    return JSONResponse({"data": "Hello,World"})


routes = [
    Route('/', home),
]

app = Starlette(debug=True, routes=routes)
