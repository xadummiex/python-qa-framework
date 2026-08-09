from src.models._base_model import BaseModel


class UserLoginRequest(BaseModel):
    username: str
    password: str

    