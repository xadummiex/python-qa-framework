from http import HTTPStatus
from requests import Response
from bank_api.config import settings
from bank_api.models.user_login_request import UserLoginRequest
from bank_api.models.user_login_response import UserLoginResponse
from bank_api.old_api.requester import Requester


class UserLoginRequester(Requester):
    def post(self, user_login_request: UserLoginRequest) -> UserLoginResponse | Response:
        url = f'{self.base_url}/auth/token/login'
        response = self.session.post(
            url=url, timeout=settings.timeout,
            json=user_login_request.model_dump(),
        )
        self.http_check(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return UserLoginResponse(**response.json())
        return response
