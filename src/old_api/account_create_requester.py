from http import HTTPStatus
from requests import Response
from src.config import settings
from src.models.account_create_response import AccountCreateResponse
from src.old_api.requester import Requester


class AccountCreateRequester(Requester):
    def post(self, model=None) -> AccountCreateResponse | Response:
        url = f'{self.base_url}/account/create'
        response = self.session.post(
            url=url, timeout=settings.timeout
        )
        self.http_check(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return AccountCreateResponse(**response.json())
        return response
