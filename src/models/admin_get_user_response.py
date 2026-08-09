from pydantic import RootModel
from src.models._base_model import BaseModel


class UserListItem(BaseModel):
    id: int
    username: str
    role: str


class AdminGetUsersResponse(RootModel[list[UserListItem]]):
    pass




