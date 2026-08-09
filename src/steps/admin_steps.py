from typing import cast

import requests
from requests import Response

from src.api.crud_requester import CrudRequester
from src.api.crud_requester_validate import CrudRequesterValidate
from src.api.endpoint import Endpoint
from src.checks import HttpCheck
from src.models.user_create_request import UserCreateRequest
from src.models.user_create_response import UserCreateResponse
from src.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def __init__(self, session: requests.Session, created_obj: list):
        super().__init__(created_obj)
        self.session = session

    def create_user(self, user_create_request: UserCreateRequest) -> UserCreateResponse:
        response = CrudRequesterValidate(session=self.session,
                                         endpoint=Endpoint.ADMIN_CREATE_USER,
                                         http_check=HttpCheck.assert_ok(),
                                         ).post(user_create_request)

        self.created_obj.append(response)
        return cast(UserCreateResponse, response)

    def create_user_invalid(self, user_create_request: UserCreateRequest):
        CrudRequester(session=self.session,
                      endpoint=Endpoint.ADMIN_CREATE_USER,
                      http_check=HttpCheck.assert_bad_request(),
                      ).post(user_create_request)

    def delete_user(self, user_id: int) -> Response:
        response = CrudRequester(session=self.session,
                                 endpoint=Endpoint.ADMIN_DELETE_USER,
                                 http_check=HttpCheck.assert_ok()
                                 ).delete(user_id)
        return response
