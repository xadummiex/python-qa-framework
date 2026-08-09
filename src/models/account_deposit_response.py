from src.models._base_model import BaseModel


class AccountDepositResponse(BaseModel):
    id: int
    balance: float
