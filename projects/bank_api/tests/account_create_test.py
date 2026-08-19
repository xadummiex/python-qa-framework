import pytest
from sqlalchemy.orm import Session

from bank_api.api_manager import ApiManager
from bank_api.db.crud.account import AccountCrudDb as Account
from bank_api.models.user_create_request import UserCreateRequest


@pytest.mark.account
class TestAccountCreate:
    def test_account_create(self, created_user: UserCreateRequest, api_manager: ApiManager, db_session: Session):
        account_create_response = api_manager.user_steps.create_account(created_user)

        assert account_create_response.balance == 0, "New account must start with zero balance"
        assert account_create_response.number, "Account number must not be empty"

        account_from_db = Account.get_account_by_id(db_session, account_create_response.id)
        assert account_from_db.id == account_create_response.id, "Account not found in db"
