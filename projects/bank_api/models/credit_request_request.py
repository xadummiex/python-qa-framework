from typing import Annotated

from bank_api.generators.creation_rule import CreationRule
from bank_api.models._base_model import BaseModel


class CreditRequestRequest(BaseModel):
    accountId: int
    # 5000.00-15000.00
    amount: Annotated[float, CreationRule(regex=r"^(([5-9][0-9]{3}|1[0-4][0-9]{3})\.[0-9]{2}|15000\.00)$")]
    termMonths: Annotated[int, CreationRule(regex=r"^([1-9]|1[0-2])$")]  # 1-12
