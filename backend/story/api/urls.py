from .views import (
    CreateStory
)
from starlette.routing import Route


routes = [
    Route('/story', CreateStory),
]
