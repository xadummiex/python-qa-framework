import logging
from typing import Any, Callable
import requests
from src.models.user_create_response import UserCreateResponse
from src.steps.admin_steps import AdminSteps
from src.steps.auth_steps import AuthSteps
from src.steps.user_steps import UserSteps


class ApiManager:
    def __init__(self, admin_session: requests.Session, make_session: Callable,
                 created_obj: list[Any]):

        self.created_obj = created_obj
        self.admin_steps = AdminSteps(admin_session, created_obj)
        self.user_steps = UserSteps(make_session, created_obj)
        self.auth_steps = AuthSteps(make_session, created_obj)

    def cleanup(self) -> None:
        for obj in reversed(self.created_obj):
            try:
                self._delete(obj)
            except Exception:
                logging.exception("Не удалось удалить %r", obj)
        self.created_obj.clear()

    def _delete(self, obj: Any) -> None:
        if isinstance(obj, UserCreateResponse):
            self.admin_steps.delete_user(obj.id)
        else:
            logging.warning("Нет правила удаления для %s", type(obj).__name__)
