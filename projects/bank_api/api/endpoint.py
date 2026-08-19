from enum import Enum
from typing import Type
from dataclasses import dataclass

from bank_api.models._base_model import BaseModel
from bank_api.models.account_deposit_request import AccountDepositRequest
from bank_api.models.account_deposit_response import AccountDepositResponse
from bank_api.models.account_create_response import AccountCreateResponse
from bank_api.models.account_transfer_request import AccountTransferRequest
from bank_api.models.account_transfer_response import AccountTransferResponse
from bank_api.models.admin_get_user_response import AdminGetUsersResponse
from bank_api.models.credit_repay_request import CreditRepayRequest
from bank_api.models.credit_repay_response import CreditRepayResponse
from bank_api.models.credit_request_request import CreditRequestRequest
from bank_api.models.credit_request_response import CreditRequestResponse
from bank_api.models.user_create_request import UserCreateRequest
from bank_api.models.user_create_response import UserCreateResponse
from bank_api.models.user_login_request import UserLoginRequest
from bank_api.models.user_login_response import UserLoginResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Type[BaseModel] | None = None
    response_model: Type[BaseModel] | None = None


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        url="/admin/create",
        request_model=UserCreateRequest,
        response_model=UserCreateResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        url="/admin/users"
    )

    ADMIN_GET_USER = EndpointConfiguration(
        url="/admin/users",
        response_model=AdminGetUsersResponse
    )

    AUTH_LOGIN = EndpointConfiguration(
        url="/auth/token/login",
        request_model=UserLoginRequest,
        response_model=UserLoginResponse,
    )

    ACCOUNT_CREATE = EndpointConfiguration(
        url="/account/create",
        response_model=AccountCreateResponse,
    )

    ACCOUNT_DEPOSIT = EndpointConfiguration(
        url="/account/deposit",
        request_model=AccountDepositRequest,
        response_model=AccountDepositResponse
    )

    ACCOUNT_TRANSFER = EndpointConfiguration(
        url="/account/transfer",
        request_model=AccountTransferRequest,
        response_model=AccountTransferResponse
    )

    CREDIT_REQUEST = EndpointConfiguration(
        url="/credit/request",
        request_model=CreditRequestRequest,
        response_model=CreditRequestResponse
    )

    CREDIT_REPAY = EndpointConfiguration(
        url="/credit/repay",
        request_model=CreditRepayRequest,
        response_model=CreditRepayResponse
    )
