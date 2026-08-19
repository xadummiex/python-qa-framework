from sqlalchemy import create_engine, text
from bank_api.config import settings


def get_engine():
    return create_engine(settings.db_url)


def clean_database(engine):
    with engine.begin() as conn:
        conn.execute(text('TRUNCATE "transaction", "credit", "account" RESTART IDENTITY CASCADE'))
        conn.execute(text("DELETE FROM \"user\" WHERE username != 'admin'"))