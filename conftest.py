import pytest
pytest.register_assert_rewrite("src.checks")


pytest_plugins = [
    "src.fixtures.db",
    "src.fixtures.sessions",
    "src.fixtures.api",
    "src.fixtures.data",
]
