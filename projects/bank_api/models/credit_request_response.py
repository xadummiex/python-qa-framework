from bank_api.models._base_model import BaseModel


class CreditRequestResponse(BaseModel):
    id: int
    amount: float
    termMonths: int
    balance: float
    creditId: int
