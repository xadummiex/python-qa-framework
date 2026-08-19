import pytest

from bank_api.api_manager import ApiManager
from bank_api.config import settings
from bank_api.models.user_create_request import UserCreateRequest
from bank_api.models.user_login_request import UserLoginRequest


@pytest.mark.auth
class TestUserLogin:
    def test_admin_login(self, api_manager: ApiManager):
        user_login_request = UserLoginRequest(username=settings.admin_username, password=settings.admin_password)
        response = api_manager.auth_steps.login(user_login_request)

        assert response.token, "Login response must contain a token"
        assert response.user.role == "ROLE_ADMIN", "Admin must keep the admin role after login"

    def test_user_login(self, api_manager: ApiManager, created_user: UserCreateRequest):
        user_login_request = UserLoginRequest(username=created_user.username, password=created_user.password)
        response = api_manager.auth_steps.login(user_login_request)

        assert response.token, "Login response must contain a token"
        assert response.user.username == created_user.username, "Token must be issued to the requested user"
