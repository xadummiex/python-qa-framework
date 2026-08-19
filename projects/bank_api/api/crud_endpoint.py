from typing import Protocol
from requests import Response
from bank_api.models._base_model import BaseModel


class CrudEndpoint(Protocol):
    def post(self, model: BaseModel | None) -> BaseModel | Response: ...
    def get(self, user_id: int) -> BaseModel | Response: ...
    def delete(self, user_id: int) -> BaseModel | Response: ...
    