import pytest
from sqlalchemy.orm import Session

from bank_api.api_manager import ApiManager
from bank_api.db.crud.credit import CreditCrudDb as Credit
from bank_api.models.account_create_response import AccountCreateResponse
from bank_api.models.credit_repay_request import CreditRepayRequest
from bank_api.models.credit_request_response import CreditRequestResponse
from bank_api.models.user_create_request import UserCreateRequest


@pytest.mark.credit
class TestCreditRepay:
    def test_credit_repay_valid(self, api_manager: ApiManager, created_credit_user: UserCreateRequest,
                                created_credit_account: AccountCreateResponse,
                                issued_credit: CreditRequestResponse, db_session: Session):
        credit_repay_request = CreditRepayRequest(creditId=issued_credit.creditId,
                                                  accountId=created_credit_account.id,
                                                  amount=issued_credit.amount)

        credit_repay_response = api_manager.user_steps.repay_credit_valid(created_credit_user, credit_repay_request)

        credit_from_db = Credit.get_credit_by_account_id(db_session, created_credit_account.id)

        assert credit_repay_response.amountDeposited == issued_credit.amount, "Deposited amount must equal the repaid amount"
        assert credit_from_db.balance == 0, "Fully repaid credit must have zero balance in db"

    def test_credit_repay_invalid(self, api_manager: ApiManager, created_credit_user: UserCreateRequest, db_session: Session,
                                  created_credit_account: AccountCreateResponse, issued_credit: CreditRequestResponse):
        credit_repay_request = CreditRepayRequest(creditId=issued_credit.creditId + 1,
                                                  accountId=created_credit_account.id,
                                                  amount=issued_credit.amount)

        api_manager.user_steps.repay_credit_not_found(created_credit_user, credit_repay_request)

        credit_from_db = Credit.get_credit_by_account_id(db_session, created_credit_account.id)

        assert credit_from_db.balance == -issued_credit.amount, "Repayment of non-existent credit must not change the debt"
