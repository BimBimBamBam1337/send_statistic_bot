from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    token: str

    postgres_dsn: str
    db_user: str
    db_pass: str
    db_name: str
    redis_port: int
    api_key: str
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = _Settings()
