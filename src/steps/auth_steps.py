from typing import Any, Callable, cast

from src.api.crud_requester_validate import CrudRequesterValidate
from src.api.endpoint import Endpoint
from src.checks import HttpCheck
from src.models.user_login_request import UserLoginRequest
from src.models.user_login_response import UserLoginResponse
from src.steps.base_steps import BaseSteps


class AuthSteps(BaseSteps):
    def __init__(self, make_session: Callable, created_obj: list[Any]):
        super().__init__(created_obj)
        self.make_session = make_session

    def login(self, user_login_request: UserLoginRequest) -> UserLoginResponse:
        response = CrudRequesterValidate(session=self.make_session(),
                                         endpoint=Endpoint.AUTH_LOGIN,
                                         http_check=HttpCheck.assert_ok(),
                                         ).post(user_login_request)

        return cast(UserLoginResponse, response)

