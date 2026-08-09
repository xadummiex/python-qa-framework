import pytest
from src.config import settings
from src.models.user_login_request import UserLoginRequest


@pytest.mark.auth
class TestUserLogin:
    def test_admin_login(self, api_manager):

        user_login_request = UserLoginRequest(username=settings.admin_username, password=settings.admin_password)
        response = api_manager.auth_steps.login(user_login_request)

        assert response.token
        assert response.user.username == settings.admin_username
        assert response.user.role == "ROLE_ADMIN"

    def test_user_login(self, api_manager, created_user):

        user_login_request = UserLoginRequest(username=created_user.username, password=created_user.password)
        response = api_manager.auth_steps.login(user_login_request)

        assert response.token
        assert response.user.username == created_user.username
        assert response.user.role == created_user.role
