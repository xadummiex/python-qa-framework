from sqlalchemy import Integer, Column, ForeignKey, Float, DateTime, String

from bank_api.db.base import Base


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, autoincrement=True)
    to_account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    from_account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    credit_id = Column(Integer, ForeignKey("credit.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return (f"<Transactions({self.id=}, {self.to_account_id=}, {self.from_account_id=}, {self.credit_id=}"
                f", {self.amount=}, {self.transaction_type=}, {self.created_at=})>")
