import pytest
from sqlalchemy.orm import Session

from src.api_manager import ApiManager
from src.db.crud.account import AccountCrudDb as Account
from src.models.account_create_response import AccountCreateResponse
from src.models.account_transfer_request import AccountTransferRequest
from src.models.user_create_request import UserCreateRequest


@pytest.mark.account
class TestAccountTransfer:
    def test_account_transfer_valid(self, api_manager: ApiManager, created_user: UserCreateRequest,
                                    two_accounts_with_funds: tuple[AccountCreateResponse,
                                                                   AccountCreateResponse, float],
                                    db_session: Session):
        account_from, account_to, balance_before = two_accounts_with_funds
        account_transfer_request = AccountTransferRequest(fromAccountId=account_from.id,
                                                          toAccountId=account_to.id,
                                                          amount=1000)

        response = api_manager.user_steps.transfer_money(created_user, account_transfer_request)

        account_from_db = Account.get_account_by_id(db_session, account_from.id)
        account_to_db = Account.get_account_by_id(db_session, account_to.id)

        assert response.fromAccountIdBalance == balance_before - account_transfer_request.amount, \
            "Sender balance must be reduced by the transferred amount"
        assert account_from_db.balance == response.fromAccountIdBalance, \
            "Db balance of the sender must match the api response"
        assert account_to_db.balance == account_transfer_request.amount, \
            "Receiver must get exactly the transferred amount"

    def test_account_transfer_invalid(self, api_manager: ApiManager, created_user: UserCreateRequest, db_session: Session,
                                      two_accounts_with_funds: tuple[AccountCreateResponse, AccountCreateResponse, float]):
        account_from, account_to, balance_before = two_accounts_with_funds
        account_transfer_request = AccountTransferRequest(fromAccountId=account_from.id,
                                                          toAccountId=account_to.id,
                                                          amount=200)

        api_manager.user_steps.transfer_money_invalid(created_user, account_transfer_request)

        account_from_db = Account.get_account_by_id(db_session, account_from.id)
        account_to_db = Account.get_account_by_id(db_session, account_to.id)

        assert account_from_db.balance == balance_before, "Rejected transfer must not withdraw money from the sender"
        assert account_to_db.balance == 0, "Rejected transfer must not credit the receiver"
