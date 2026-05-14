from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://collie:collie_secret@localhost:5432/collie_db"

    @model_validator(mode="after")
    def fix_database_url(self) -> "Settings":
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        self.database_url = url
        return self

    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # App
    app_env: str = "development"
    app_debug: bool = True
    cors_origins: str = "http://localhost:5173"

    # Collie App
    collie_app_base_url: str = "https://api.collieapp.com"
    collie_app_client_id: str = ""
    collie_app_client_secret: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
