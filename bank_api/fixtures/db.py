import pytest
from bank_api.db.engine import SessionLocal, engine
from bank_api.db.db import clean_database, get_engine


@pytest.fixture(scope="session")
def db_engine():
    engine = get_engine()
    yield engine
    engine.dispose()


# включить - добавить autouse=True.
@pytest.fixture(scope="session")
def clean_db(db_engine):
    clean_database(db_engine)
    yield


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
