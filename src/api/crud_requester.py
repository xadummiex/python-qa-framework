from requests import Response
from src.api.http_requester import HttpRequester
from src.config import settings
from src.models._base_model import BaseModel
import allure


class CrudRequester(HttpRequester):
    def get(self) -> Response:
        response = self.session.get(
            url=f'{self.base_url}{self.endpoint.value.url}', timeout=settings.timeout,
        )
        self.http_check(response)
        return response

    def post(self, model: BaseModel | None = None) -> Response:
        body = model.model_dump() if model is not None else None

        with allure.step(f'POST {self.base_url}{self.endpoint.value.url}'):
            allure.attach(str(body), "Request body", allure.attachment_type.JSON)

        response = self.session.post(
            url=f'{self.base_url}{self.endpoint.value.url}', timeout=settings.timeout,
            json=body,
        )

        allure.attach(str(response), "Response body", allure.attachment_type.JSON)

        self.http_check(response)
        return response

    def delete(self, user_id: int) -> Response:
        response = self.session.delete(
            url=f'{self.base_url}{self.endpoint.value.url}/{user_id}', timeout=settings.timeout,
        )
        self.http_check(response)
        return response


