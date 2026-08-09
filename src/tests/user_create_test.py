import pytest
from sqlalchemy.orm import Session

from src.db.crud.user import UserCrudDb as User
from src.fixtures.db import db_session
from src.generators.model_generator import RandomModelGenerator
from src.models.user_create_request import UserCreateRequest


@pytest.mark.admin
class TestUserCreate:

    @pytest.mark.parametrize("user_create_request", [RandomModelGenerator.generate(UserCreateRequest)])
    def test_user_create_valid(self, api_manager, user_create_request, db_session):

        user_create_response = api_manager.admin_steps.create_user(user_create_request)

        assert user_create_request.username == user_create_response.username
        assert user_create_request.role == user_create_response.role

        user_from_db = User.get_user_by_username(db_session, user_create_request.username)
        assert user_from_db.username == user_create_request.username, "User not in db"

    @pytest.mark.parametrize("username, password", [
        # invalid username
        ("макс1", "Pas!sw0rd"),
        ("M1", "Pas!sw0rd"),
        ("Maximilianus1111", "Pas!sw0rd"),
        ("Max1!", "Pas!sw0rd"),
        # invalid password
        ("Max3", "Pas!sw0rд"),
        ("Max4", "Pas!sw0"),
        ("Max5", "pas!sw0rd"),
        ("Max6", "Pas1sw0rd"),
        ("Max7", "Pas!sword"),
    ])
    def test_user_create_invalid(self, username, password, api_manager, db_session):
        user_create_request = UserCreateRequest(username=username, password=password, role="ROLE_USER")

        api_manager.admin_steps.create_user_invalid(user_create_request)

        user_from_db = User.get_user_by_username(db_session, user_create_request.username)
        assert user_from_db is None, "User created, in db"



