from http import HTTPStatus
from requests import Response
from src.config import settings
from src.models.user_login_request import UserLoginRequest
from src.models.user_login_response import UserLoginResponse
from src.old_api.requester import Requester


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
