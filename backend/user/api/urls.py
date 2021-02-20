from .views import (
    UserRegister, Auth
)
from starlette.routing import Route


routes = [
    Route('/user/register', UserRegister),
    Route('/user/auth', Auth),
]
