from typing import Annotated

from src.generators.creation_rule import CreationRule
from src.models._base_model import BaseModel


class AccountTransferRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: Annotated[float, CreationRule(
        regex=r"^(500\.[0-9]{2}|[5-9][0-9]{2}\.[0-9]{2}|[1-9][0-9]{3}\.[0-9]{2}|10000\.00)$")]  # 500 - 10000
