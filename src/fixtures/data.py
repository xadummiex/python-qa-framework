import pytest

from src.generators.model_generator import RandomModelGenerator
from src.models.user_create_request import UserCreateRequest


@pytest.fixture
def created_user(api_manager) -> UserCreateRequest:
    user_create_request = RandomModelGenerator.generate(UserCreateRequest)
    api_manager.admin_steps.create_user(user_create_request)
    return user_create_request


@pytest.fixture
def created_credit_user(api_manager) -> UserCreateRequest:
    user_create_request = RandomModelGenerator.generate(UserCreateRequest, role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(user_create_request)
    return user_create_request
