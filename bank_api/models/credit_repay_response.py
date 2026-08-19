from bank_api.models._base_model import BaseModel


class CreditRepayResponse(BaseModel):
    creditId: int
    amountDeposited: float
