import pytest
from bank_api.api_manager import ApiManager


@pytest.fixture
def created_obj() -> list:
    return []


@pytest.fixture
def api_manager(admin_session, make_session, created_obj):
    manager = ApiManager(admin_session, make_session, created_obj)
    yield manager
    manager.cleanup()
