from sqlalchemy.orm import Session

from bank_api.db.tables.account import Account


class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db_session: Session, account_id: str) -> Account | None:
        return db_session.query(Account).filter_by(id=account_id).first()
