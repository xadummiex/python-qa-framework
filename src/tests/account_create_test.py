import pytest

from src.db.crud.account import AccountCrudDb as Account


@pytest.mark.account
class TestAccountCreate:
    def test_account_create(self, created_user, api_manager, db_session):

        account_create_response = api_manager.user_steps.create_account(created_user)

        assert account_create_response.balance == 0
        assert account_create_response.number

        account_from_db = Account.get_account_by_id(db_session, account_create_response.id)
        assert account_from_db.id == account_create_response.id, "Account creation failed, no account in db"
        assert account_from_db.balance is not None, "Balance was None for account creation"
