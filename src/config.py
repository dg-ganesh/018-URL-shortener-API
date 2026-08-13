"""
Project : URL Shortener API

Project ID : 018

Application Configuration
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Central application configuration."""

    # Application
    project_id: str = "018"
    project_name: str = "URL Shortener API"
    app_version: str = "1.0.0"
    environment: str = "development"

    # API
    api_v1_prefix: str = "/api/v1"
    base_url: str = "http://localhost:8000"

    # Database
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "url_shortener"
    database_user: str = "postgres"
    database_password: str = Field(default="")
    database_ssl_mode: str = "require"

    # Runtime paths
    log_directory: Path = PROJECT_ROOT / "logs"
    execution_report_file: Path = (
        PROJECT_ROOT / "logs" / "execution_report.txt"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """Return the PostgreSQL connection URL."""
        return (
            "postgresql+psycopg://"
            f"{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}"
            f"/{self.database_name}"
            f"?sslmode={self.database_ssl_mode}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()