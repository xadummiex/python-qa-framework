from enum import Enum
from typing import Type
from dataclasses import dataclass

from src.models._base_model import BaseModel
from src.models.account_deposit_request import AccountDepositRequest
from src.models.account_deposit_response import AccountDepositResponse
from src.models.account_create_response import AccountCreateResponse
from src.models.account_transfer_request import AccountTransferRequest
from src.models.account_transfer_response import AccountTransferResponse
from src.models.admin_get_user_response import AdminGetUsersResponse
from src.models.credit_repay_request import CreditRepayRequest
from src.models.credit_repay_response import CreditRepayResponse
from src.models.credit_request_request import CreditRequestRequest
from src.models.credit_request_response import CreditRequestResponse
from src.models.user_create_request import UserCreateRequest
from src.models.user_create_response import UserCreateResponse
from src.models.user_login_request import UserLoginRequest
from src.models.user_login_response import UserLoginResponse


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
