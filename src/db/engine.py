from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

engine = create_engine(settings.db_url, echo=False)
SessionLocal = sessionmaker(bind=engine)

