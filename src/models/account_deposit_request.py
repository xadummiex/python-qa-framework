from typing import Annotated

from src.generators.creation_rule import CreationRule
from src.models._base_model import BaseModel


class AccountDepositRequest(BaseModel):
    accountId: int
    amount: Annotated[float, CreationRule(regex=r"^[1-8][0-9]{3}\.[0-9]{2}$")]
