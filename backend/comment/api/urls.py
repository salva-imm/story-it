from .views import (
    CreateComment
)

from starlette.routing import Route

routes = [
    Route('/comment', CreateComment),
]
