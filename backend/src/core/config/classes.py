from typing import Literal

from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

type LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class BaseConfiguration(BaseSettings):
    """Base settings configuration class."""

    model_config = SettingsConfigDict(
        env_file=("../.env",),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="BACKEND__",
        frozen=True,
        extra="ignore",
    )


class LoggingSettings(BaseModel):
    """Logging settings configuration."""

    log_level: LogLevel = "DEBUG"
    log_format: str = "%(asctime)s %(levelname)6s %(name)s: %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"
    sentry_dsn: HttpUrl | None = None
    sentry_traces_sample_rate: float = 1.0
    sentry_log_level: LogLevel = "ERROR"


class ProjectSettings(BaseModel):
    """Project settings configuration."""

    project_name: str
    description: str
    docs_url: str = "/docs"
    openapi_url: str = "/docs/openapi.json"
    redoc_url: str = "/re-docs"

    @property
    def title(self) -> str:
        """Return project title."""
        return f"{self.project_name} - Swagger UI"
