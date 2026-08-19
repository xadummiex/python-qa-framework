from bank_api.models._base_model import BaseModel


class AccountTransferResponse(BaseModel):
    fromAccountId: int
    toAccountId: int
    fromAccountIdBalance: float
