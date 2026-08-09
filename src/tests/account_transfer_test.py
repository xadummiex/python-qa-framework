import pytest

from src.db.crud.account import AccountCrudDb as Account
from src.models.account_deposit_request import AccountDepositRequest
from src.models.account_transfer_request import AccountTransferRequest


@pytest.mark.account
class TestAccountTransfer:
    def test_account_transfer_valid(self, api_manager, created_user, db_session):

        account1 = api_manager.user_steps.create_account(created_user)
        account2 = api_manager.user_steps.create_account(created_user)

        account1_from_db = Account.get_account_by_id(db_session, account1.id)
        account2_from_db = Account.get_account_by_id(db_session, account2.id)

        account1_deposit_request = AccountDepositRequest(accountId=account1.id, amount=2222)
        api_manager.user_steps.deposit_account(created_user, account1_deposit_request)

        account1_transfer_request = AccountTransferRequest(fromAccountId=account1.id,
                                                           toAccountId=account2.id,
                                                           amount=1000)

        response = api_manager.user_steps.transfer_money(created_user, account1_transfer_request)
        db_session.refresh(account1_from_db)
        db_session.refresh(account2_from_db)

        account1_new_balance = account1_deposit_request.amount - account1_transfer_request.amount

        assert account1.id == response.fromAccountId
        assert account2.id == response.toAccountId
        assert response.fromAccountIdBalance == account1_new_balance
        assert account1_from_db.balance == account1_new_balance
        assert account2_from_db.balance == account1_transfer_request.amount

    def test_account_transfer_invalid(self, api_manager, created_user, db_session):

        account1 = api_manager.user_steps.create_account(created_user)
        account2 = api_manager.user_steps.create_account(created_user)

        account1_from_db = Account.get_account_by_id(db_session, account1.id)
        account2_from_db = Account.get_account_by_id(db_session, account2.id)

        account_deposit_request = AccountDepositRequest(accountId=account1.id, amount=2222)
        api_manager.user_steps.deposit_account(created_user, account_deposit_request)

        account_transfer_request = AccountTransferRequest(fromAccountId=account1.id,
                                                          toAccountId=account2.id,
                                                          amount=200)

        api_manager.user_steps.transfer_money_invalid(created_user, account_transfer_request)
        db_session.refresh(account1_from_db)
        db_session.refresh(account2_from_db)

        assert account1_from_db.balance == account_deposit_request.amount
        assert account2_from_db.balance == 0

