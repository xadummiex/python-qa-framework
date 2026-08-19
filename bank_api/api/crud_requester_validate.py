from typing import Callable

import allure
import requests
from bank_api.api.crud_requester import CrudRequester
from bank_api.api.endpoint import Endpoint
from bank_api.api.http_requester import HttpRequester
from bank_api.config import settings
from bank_api.models._base_model import BaseModel


class CrudRequesterValidate(HttpRequester):
    def __init__(self, session: requests.Session, endpoint: Endpoint,
                 http_check: Callable, base_url: str = settings.base_url):

        super().__init__(session, endpoint, http_check, base_url)
        self.crud_requester = CrudRequester(session, endpoint, http_check, base_url)

    def post(self, model: BaseModel | None = None) -> BaseModel:
        response = self.crud_requester.post(model)
        with allure.step(f'POST {self.base_url}{self.endpoint.value.url} and Validated Model'):
            allure.attach(f'Validated Model response: {self.endpoint.value.response_model.__name__}')

        return self.endpoint.value.response_model.model_validate(response.json())

    def get(self):
        response = self.crud_requester.get()

        return self.endpoint.value.response_model.model_validate(response.json())

    