import requests
from abc import ABC, abstractmethod
from typing import Callable
from bank_api.config import settings
from bank_api.models._base_model import BaseModel


class Requester(ABC):
    def __init__(self,
                 session: requests.Session,
                 http_check: Callable,
                 base_url: str = settings.base_url):
        self.session = session
        self.base_url = base_url
        self.http_check = http_check

    @abstractmethod
    def post(self, model: BaseModel):
        ...
