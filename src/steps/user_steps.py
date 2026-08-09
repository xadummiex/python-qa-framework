from typing import cast

from src.api.crud_requester import CrudRequester
from src.api.crud_requester_validate import CrudRequesterValidate
from src.api.endpoint import Endpoint
from src.checks import HttpCheck
from src.models.account_create_response import AccountCreateResponse
from src.models.account_deposit_request import AccountDepositRequest
from src.models.account_deposit_response import AccountDepositResponse
from src.models.account_transfer_request import AccountTransferRequest
from src.models.account_transfer_response import AccountTransferResponse
from src.models.credit_repay_response import CreditRepayResponse
from src.models.credit_request_request import CreditRequestRequest
from src.models.credit_request_response import CreditRequestResponse
from src.models.user_create_request import UserCreateRequest
from src.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def __init__(self, make_session, created_obj: list):
        super().__init__(created_obj)
        self.make_session = make_session

    def create_account(self, created_user: UserCreateRequest) -> AccountCreateResponse:
        response = CrudRequesterValidate(session=self.make_session(created_user.username, created_user.password),
                                         endpoint=Endpoint.ACCOUNT_CREATE,
                                         http_check=HttpCheck.assert_created()
                                         ).post()
        return cast(AccountCreateResponse, response)  # cast - конкретизирую return для IDE

    def deposit_account(self, created_user: UserCreateRequest,
                        account_deposit_request: AccountDepositRequest) -> AccountDepositResponse:
        response = CrudRequesterValidate(session=self.make_session(created_user.username, created_user.password),
                                         endpoint=Endpoint.ACCOUNT_DEPOSIT,
                                         http_check=HttpCheck.assert_ok()
                                         ).post(account_deposit_request)
        return cast(AccountDepositResponse, response)

    def deposit_account_invalid(self, created_user: UserCreateRequest, account_deposit_request: AccountDepositRequest):
        CrudRequester(session=self.make_session(created_user.username, created_user.password),
                      endpoint=Endpoint.ACCOUNT_DEPOSIT,
                      http_check=HttpCheck.assert_bad_request()
                      ).post(account_deposit_request)

    def transfer_money(self, created_user: UserCreateRequest,
                       account_transfer_request: AccountTransferRequest) -> AccountTransferResponse:
        response = CrudRequesterValidate(session=self.make_session(created_user.username, created_user.password),
                                         endpoint=Endpoint.ACCOUNT_TRANSFER,
                                         http_check=HttpCheck.assert_ok()
                                         ).post(account_transfer_request)
        return cast(AccountTransferResponse, response)

    def transfer_money_invalid(self, created_user: UserCreateRequest, account_transfer_request: AccountTransferRequest):
        CrudRequester(session=self.make_session(created_user.username, created_user.password),
                      endpoint=Endpoint.ACCOUNT_TRANSFER,
                      http_check=HttpCheck.assert_bad_request()
                      ).post(account_transfer_request)

    def request_credit_valid(self, created_credit_user: UserCreateRequest,
                             credit_request_request: CreditRequestRequest) -> CreditRequestResponse:
        response = CrudRequesterValidate(session=self.make_session(created_credit_user.username,
                                                                   created_credit_user.password),
                                         endpoint=Endpoint.CREDIT_REQUEST,
                                         http_check=HttpCheck.assert_created()
                                         ).post(credit_request_request)

        return cast(CreditRequestResponse, response)

    def request_credit_invalid(self, created_credit_user: UserCreateRequest,
                               credit_request_request: CreditRequestRequest):
        CrudRequester(session=self.make_session(created_credit_user.username, created_credit_user.password),
                      endpoint=Endpoint.CREDIT_REQUEST,
                      http_check=HttpCheck.assert_bad_request()
                      ).post(credit_request_request)

    def repay_credit_valid(self, created_credit_user: UserCreateRequest,
                           credit_repay_request: CreditRequestRequest) -> CreditRepayResponse:
        response = CrudRequesterValidate(session=self.make_session(created_credit_user.username,
                                                                   created_credit_user.password),
                                         endpoint=Endpoint.CREDIT_REPAY,
                                         http_check=HttpCheck.assert_ok()
                                         ).post(credit_repay_request)

        return cast(CreditRepayResponse, response)

    def repay_credit_not_found(self, created_credit_user: UserCreateRequest, credit_repay_request):
        CrudRequester(session=self.make_session(created_credit_user.username,
                                                created_credit_user.password),
                      endpoint=Endpoint.CREDIT_REPAY,
                      http_check=HttpCheck.assert_not_found()
                      ).post(credit_repay_request)

