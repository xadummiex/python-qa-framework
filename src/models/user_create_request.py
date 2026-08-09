from typing import Annotated

from src.generators.creation_rule import CreationRule
from src.models._base_model import BaseModel


class UserCreateRequest(BaseModel):
    username: Annotated[str, CreationRule(regex=r"^[A-Za-z0-9]{3,15}$")]
    password: Annotated[str, CreationRule(regex=r"^[A-Z]{2}[a-z]{4}\d{2}[!@#$%_]{2}$")]
    role: Annotated[str, CreationRule(regex=r"ROLE_USER")]
