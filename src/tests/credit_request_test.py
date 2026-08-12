import pytest
from sqlalchemy.orm import Session

from src.api_manager import ApiManager
from src.db.crud.account import AccountCrudDb as Account
from src.db.crud.credit import CreditCrudDb as Credit
from src.generators.model_generator import RandomModelGenerator
from src.models.account_create_response import AccountCreateResponse
from src.models.credit_request_request import CreditRequestRequest
from src.models.user_create_request import UserCreateRequest


@pytest.mark.credit
class TestCreditRequest:
    def test_credit_request_valid(self, api_manager: ApiManager, created_credit_user: UserCreateRequest,
                                  created_credit_account: AccountCreateResponse, db_session: Session):
        credit_request_request = RandomModelGenerator.generate(CreditRequestRequest, accountId=created_credit_account.id)

        credit_request_response = api_manager.user_steps.request_credit_valid(created_credit_user, credit_request_request)

        credit_from_db = Credit.get_credit_by_account_id(db_session, created_credit_account.id)

        assert credit_request_response.balance == credit_request_request.amount, "Account balance must grow by the credit amount"
        assert credit_request_response.creditId, "Response must contain the credit id"
        assert credit_from_db.amount == credit_request_request.amount, "Db credit amount must equal the requested amount"

    @pytest.mark.parametrize("amount, term_months", [
        (4999, 1),
        (15001, 2),
        (-10000, 3),
        (0, 4),
        (7000, 0),
    ])
    def test_credit_request_invalid(self, api_manager: ApiManager, created_credit_user: UserCreateRequest,
                                    created_credit_account: AccountCreateResponse, amount: float,
                                    term_months: int, db_session: Session):
        credit_request_request = CreditRequestRequest(accountId=created_credit_account.id, amount=amount,
                                                      termMonths=term_months)

        api_manager.user_steps.request_credit_invalid(created_credit_user, credit_request_request)

        account_from_db = Account.get_account_by_id(db_session, created_credit_account.id)

        assert account_from_db.balance == 0, "Rejected credit must not change the account balance"
