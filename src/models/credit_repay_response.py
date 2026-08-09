from src.models._base_model import BaseModel


class CreditRepayResponse(BaseModel):
    creditId: int
    amountDeposited: float
