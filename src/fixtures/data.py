import pytest

from src.api_manager import ApiManager
from src.generators.model_generator import RandomModelGenerator
from src.models.account_create_response import AccountCreateResponse
from src.models.account_deposit_request import AccountDepositRequest
from src.models.credit_request_request import CreditRequestRequest
from src.models.credit_request_response import CreditRequestResponse
from src.models.user_create_request import UserCreateRequest


@pytest.fixture
def created_user(api_manager: ApiManager) -> UserCreateRequest:
    user_create_request = RandomModelGenerator.generate(UserCreateRequest)
    api_manager.admin_steps.create_user(user_create_request)
    return user_create_request


@pytest.fixture
def created_credit_user(api_manager: ApiManager) -> UserCreateRequest:
    user_create_request = RandomModelGenerator.generate(UserCreateRequest, role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(user_create_request)
    return user_create_request


@pytest.fixture
def created_account(api_manager: ApiManager, created_user: UserCreateRequest) -> AccountCreateResponse:
    return api_manager.user_steps.create_account(created_user)


@pytest.fixture
def created_credit_account(api_manager: ApiManager,
                           created_credit_user: UserCreateRequest) -> AccountCreateResponse:
    return api_manager.user_steps.create_account(created_credit_user)


@pytest.fixture
def two_accounts_with_funds(api_manager: ApiManager,
                            created_user: UserCreateRequest) -> tuple[AccountCreateResponse,
                                                                      AccountCreateResponse, float]:
    account_from = api_manager.user_steps.create_account(created_user)
    account_to = api_manager.user_steps.create_account(created_user)

    account_deposit_request = RandomModelGenerator.generate(AccountDepositRequest, accountId=account_from.id)
    account_deposit_response = api_manager.user_steps.deposit_account(created_user, account_deposit_request)

    return account_from, account_to, account_deposit_response.balance


@pytest.fixture
def issued_credit(api_manager: ApiManager, created_credit_user: UserCreateRequest,
                  created_credit_account: AccountCreateResponse) -> CreditRequestResponse:
    credit_request_request = RandomModelGenerator.generate(CreditRequestRequest,
                                                           accountId=created_credit_account.id)
    return api_manager.user_steps.request_credit_valid(created_credit_user, credit_request_request)
