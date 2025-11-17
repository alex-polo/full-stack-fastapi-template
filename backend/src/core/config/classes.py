from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfiguration(BaseSettings):
    """Base settings configuration class."""

    model_config = SettingsConfigDict(env_file=".env")
