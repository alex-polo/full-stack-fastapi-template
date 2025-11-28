from typing import Literal

from pydantic import (
    BaseModel,
    HttpUrl,
    PostgresDsn,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

type LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class BaseConfiguration(BaseSettings):
    """Base settings configuration class."""

    model_config = SettingsConfigDict(
        env_file=(
            "../.env.template",
            "../.env.local",
        ),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="BACKEND__",
        frozen=True,
        extra="ignore",
    )


class LggingSettings(BaseModel):
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


class ApiV1Prefix(BaseModel):
    """API v1 prefix configuration."""

    prefix: str = "/v1"


class ApiPrefix(BaseModel):
    """API prefix configuration."""

    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseSettings(BaseModel):
    """Database settings configuration."""

    host: str
    port: int
    user: str
    user_password: str
    db_name: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    pool_pre_ping: bool = True
    pool_recycle: int = 3600
    autoflush: bool = False
    autocommit: bool = False
    expire_on_commit: bool = False

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_uri(self) -> PostgresDsn:
        """Get PostgreSQL DSN."""
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.user_password,
            host=self.host,
            port=self.port,
            path=self.db_name,
        )


class GunicornSettings(BaseModel):
    """Gunicorn settings configuration."""

    host: str
    port: int
    workers: int = 1
    timeout: int = 60
    worker_class: str = "uvicorn.workers.UvicornWorker"
    access_log: str = "-"
    error_log: str = "-"
    log_level: LogLevel = "INFO"


class ServerSettings(BaseConfiguration):
    """Server settings configuration."""

    ENVIRONMENT: Literal["local", "staging", "prod"]
    PROJECT: ProjectSettings
    DATABASE: DatabaseSettings
    GUNICORN: GunicornSettings
    API_PREFIX: ApiPrefix = ApiPrefix()
    LOGGING: LggingSettings = LggingSettings()
