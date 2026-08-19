import pytest
pytest.register_assert_rewrite("src.checks")


pytest_plugins = [
    "bank_api.fixtures.db",
    "bank_api.fixtures.sessions",
    "bank_api.fixtures.api",
    "bank_api.fixtures.data",
]
