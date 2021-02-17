from pydantic.error_wrappers import ValidationError
from starlette.endpoints import HTTPEndpoint, HTTPException


class BaseEndpoint(HTTPEndpoint):
    def is_valid(self, **data):
        try:
            self.Arguments(**data)
        except ValidationError as v:
            raise HTTPException(detail=v.json(), status_code=400)
