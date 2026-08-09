from http import HTTPStatus
from requests import Response
from src.config import settings
from src.models.user_create_request import UserCreateRequest
from src.models.user_create_response import UserCreateResponse
from src.old_api.requester import Requester


class UserCreateRequester(Requester):
    def post(self, user_create_request: UserCreateRequest) -> UserCreateResponse | Response:
        url = f'{self.base_url}/admin/create'
        response = self.session.post(
            url=url, timeout=settings.timeout,
            json=user_create_request.model_dump(),
        )
        self.http_check(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return UserCreateResponse(**response.json())
        return response
