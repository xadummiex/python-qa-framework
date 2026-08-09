import pytest

from src.db.crud.account import AccountCrudDb as Account
from src.generators.model_generator import RandomModelGenerator
from src.models import account_deposit_response
from src.models.account_deposit_request import AccountDepositRequest


@pytest.mark.account
class TestAccountDeposit:
    def test_account_deposit_valid(self, api_manager, created_user, db_session):

        account_create_response = api_manager.user_steps.create_account(created_user)
        account_from_db = Account.get_account_by_id(db_session, account_create_response.id)
        assert account_from_db.balance == account_create_response.balance == 0

        account_deposit_request = RandomModelGenerator.generate(AccountDepositRequest,
                                                                accountId=account_create_response.id)
        account_deposit_response = api_manager.user_steps.deposit_account(created_user, account_deposit_request)

        db_session.refresh(account_from_db)

        assert account_deposit_response.id == account_create_response.id
        assert account_deposit_response.balance == account_deposit_request.amount
        assert account_from_db.balance == account_deposit_request.amount

    @pytest.mark.parametrize("amount", [-1000, -1, 0, 999, 10001])
    def test_account_deposit_invalid(self, api_manager, created_user, amount, db_session):

        account_create_response = api_manager.user_steps.create_account(created_user)
        account_from_db = Account.get_account_by_id(db_session, account_create_response.id)

        assert account_create_response.balance == account_from_db.balance == 0

        account_deposit_request = RandomModelGenerator.generate(AccountDepositRequest,
                                                                accountId=account_create_response.id,
                                                                amount=amount)
        api_manager.user_steps.deposit_account_invalid(created_user, account_deposit_request)
        db_session.refresh(account_from_db)

        assert account_from_db.balance == 0

