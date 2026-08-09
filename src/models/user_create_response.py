from src.models._base_model import BaseModel


class UserCreateResponse(BaseModel):
    id: int
    username: str
    password: str
    role: str


