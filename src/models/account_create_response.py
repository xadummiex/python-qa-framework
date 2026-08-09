from src.models._base_model import BaseModel


class AccountCreateResponse(BaseModel):
    id: int
    number: str
    balance: float
