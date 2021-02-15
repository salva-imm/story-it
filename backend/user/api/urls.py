from .views import UserRegister
from starlette.routing import Route


routes = [
    Route('/user/register', UserRegister),
]
