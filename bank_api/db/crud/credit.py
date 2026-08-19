from sqlalchemy.orm import Session
from bank_api.db.tables.credit import Credit


class CreditCrudDb:
    @staticmethod
    def get_credit_by_account_id(db: Session, account_id: int) -> Credit | None:
        return db.query(Credit).filter_by(account_id=account_id).first()







