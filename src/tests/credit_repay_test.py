import pytest

from src.db.crud.credit import CreditCrudDb as Credit
from src.generators.model_generator import RandomModelGenerator
from src.models.credit_repay_request import CreditRepayRequest
from src.models.credit_request_request import CreditRequestRequest


@pytest.mark.credit
class TestCreditRepay:
    def test_credit_repay_valid(self, api_manager, created_credit_user, db_session):

        account_create_response = api_manager.user_steps.create_account(created_credit_user)

        credit_request_request = RandomModelGenerator.generate(CreditRequestRequest,
                                                               accountId=account_create_response.id)

        credit_request_response = api_manager.user_steps.request_credit_valid(created_credit_user,
                                                                              credit_request_request)
        credit_from_db = Credit.get_credit_by_account_id(db_session, account_create_response.id)

        credit_repay_request = CreditRepayRequest(creditId=credit_request_response.creditId,
                                                  accountId=account_create_response.id,
                                                  amount=credit_request_response.amount)

        credit_repay_response = api_manager.user_steps.repay_credit_valid(created_credit_user, credit_repay_request)
        db_session.refresh(credit_from_db)

        assert credit_repay_response.creditId == credit_repay_request.creditId
        assert credit_repay_response.amountDeposited == credit_repay_request.amount
        assert credit_from_db.balance == 0

    def test_credit_repay_invalid(self, api_manager, created_credit_user, db_session):

        account_create_response = api_manager.user_steps.create_account(created_credit_user)

        credit_request_request = RandomModelGenerator.generate(CreditRequestRequest,
                                                               accountId=account_create_response.id)

        credit_request_response = api_manager.user_steps.request_credit_valid(created_credit_user,
                                                                              credit_request_request)
        credit_from_db = Credit.get_credit_by_account_id(db_session, account_create_response.id)

        credit_repay_request = CreditRepayRequest(creditId=credit_request_response.creditId+1,
                                                  accountId=account_create_response.id,
                                                  amount=credit_request_response.amount)

        api_manager.user_steps.repay_credit_not_found(created_credit_user, credit_repay_request)
        db_session.refresh(credit_from_db)

        assert credit_from_db.balance == -credit_request_request.amount

