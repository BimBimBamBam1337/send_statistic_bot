from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    token: str

    postgres_dsn: PostgresDsn
    postgres_password: str
    postgres_db: str
    postgres_user: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = _Settings()
