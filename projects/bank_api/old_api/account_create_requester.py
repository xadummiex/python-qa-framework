from http import HTTPStatus
from requests import Response
from bank_api.config import settings
from bank_api.models.account_create_response import AccountCreateResponse
from bank_api.old_api.requester import Requester


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
