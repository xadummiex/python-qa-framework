import pytest
from sqlalchemy.orm import Session

from src.api_manager import ApiManager
from src.db.crud.account import AccountCrudDb as Account
from src.generators.model_generator import RandomModelGenerator
from src.models.account_create_response import AccountCreateResponse
from src.models.account_deposit_request import AccountDepositRequest
from src.models.user_create_request import UserCreateRequest


@pytest.mark.account
class TestAccountDeposit:
    def test_account_deposit_valid(self, api_manager: ApiManager, created_user: UserCreateRequest,
                                   created_account: AccountCreateResponse, db_session: Session):
        account_deposit_request = RandomModelGenerator.generate(AccountDepositRequest,
                                                                accountId=created_account.id)

        account_deposit_response = api_manager.user_steps.deposit_account(created_user, account_deposit_request)

        account_from_db = Account.get_account_by_id(db_session, created_account.id)

        assert account_deposit_response.balance == account_deposit_request.amount, \
            "Api balance must equal the deposited amount"
        assert account_from_db.balance == account_deposit_request.amount, \
            "Db balance must equal the deposited amount"

    @pytest.mark.parametrize("amount", [-1000, -1, 0, 999, 10001])
    def test_account_deposit_invalid(self, api_manager: ApiManager, created_user: UserCreateRequest,
                                     created_account: AccountCreateResponse, amount: float,
                                     db_session: Session):
        account_deposit_request = RandomModelGenerator.generate(AccountDepositRequest, accountId=created_account.id,
                                                                amount=amount)

        api_manager.user_steps.deposit_account_invalid(created_user, account_deposit_request)

        account_from_db = Account.get_account_by_id(db_session, created_account.id)

        assert account_from_db.balance == 0, "Rejected deposit must not change the balance"
