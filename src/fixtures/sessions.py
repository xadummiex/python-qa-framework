from http import HTTPStatus
import pytest
import requests
from src.config import settings


@pytest.fixture(scope="session")
def make_session():
    sessions = []

    def _make(username=None, password=None):
        session = requests.Session()
        session.headers.update({
            "Content-Type": "application/json",
            "accept": "application/json",
        })

        if username:
            r = session.post(f"{settings.base_url}/auth/token/login",
                             json={"username": username, "password": password},
                             timeout=settings.timeout)
            assert r.status_code == HTTPStatus.OK
            session.headers["Authorization"] = f"Bearer {r.json()['token']}"

        sessions.append(session)
        return session

    yield _make
    for s in sessions:
        s.close()


@pytest.fixture(scope="session")
def admin_session(make_session):
    return make_session(settings.admin_username, settings.admin_password)
