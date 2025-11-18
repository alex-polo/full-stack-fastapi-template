from typing import Literal

from pydantic import (
    BaseModel,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfiguration(BaseSettings):
    """Base settings configuration class."""

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="BACKEND__",
        frozen=True,
        extra="ignore",

    )

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

    model_config = SettingsConfigDict(env_file=".env")
class ServerSettings(BaseConfiguration):
    """Server settings configuration."""

    ENVIRONMENT: Literal["local", "staging", "prod"]
    PROJECT: ProjectSettings
    API_PREFIX: ApiPrefix = ApiPrefix()
