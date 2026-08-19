from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = Path(__file__).resolve().parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    base_url: str = "http://localhost:4111/api"
    timeout: int = 5

    admin_username: str
    admin_password: str
    db_url: str


settings = Settings()

