import pytest

from src.db.crud.credit import CreditCrudDb as Credit
from src.generators.model_generator import RandomModelGenerator
from src.models.credit_request_request import CreditRequestRequest


@pytest.mark.credit
class TestCreditRequest:
    def test_credit_request_valid(self, created_credit_user, api_manager, db_session):

        account_create_response = api_manager.user_steps.create_account(created_credit_user)

        credit_request_request = RandomModelGenerator.generate(CreditRequestRequest,
                                                               accountId=account_create_response.id)

        credit_request_response = api_manager.user_steps.request_credit_valid(created_credit_user,
                                                                              credit_request_request)
        credit_from_db = Credit.get_credit_by_account_id(db_session, account_create_response.id)

        assert credit_request_response.id == credit_request_request.accountId
        assert credit_request_response.amount == credit_request_request.amount
        assert credit_request_response.termMonths == credit_request_request.termMonths
        assert credit_request_response.balance == credit_request_request.amount
        assert credit_request_response.creditId

        assert credit_from_db.account_id == account_create_response.id

    @pytest.mark.parametrize('amount, term_months', [
                            (4999, 1),
                            (15001, 2),
                            (-10000, 3),
                            (0, 4),
                            (7000, 0)
    ])
    def test_credit_request_invalid(self, created_credit_user, api_manager, amount, term_months, db_session):
        account_create_response = api_manager.user_steps.create_account(created_credit_user)

        credit_request_request = CreditRequestRequest(accountId=account_create_response.id,
                                                      amount=amount,
                                                      termMonths=term_months)

        api_manager.user_steps.request_credit_invalid(created_credit_user, credit_request_request)
        credit_from_db = Credit.get_credit_by_account_id(db_session, account_create_response.id)

        assert credit_from_db is None

