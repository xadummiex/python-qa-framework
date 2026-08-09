from typing import Literal
from src.models._base_model import BaseModel


class User(BaseModel):
    username: str
    role: Literal['ROLE_USER', 'ROLE_ADMIN']


class UserLoginResponse(BaseModel):
    token: str
    user: User
