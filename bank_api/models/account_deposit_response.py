from bank_api.models._base_model import BaseModel


class AccountDepositResponse(BaseModel):
    id: int
    balance: float
