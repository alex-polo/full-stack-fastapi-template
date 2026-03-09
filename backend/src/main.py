from fastapi import FastAPI

from src.core.config import APP_SETTINGS

app = FastAPI(
    title=APP_SETTINGS.PROJECT.title,
    description=APP_SETTINGS.PROJECT.description,
    docs_url=APP_SETTINGS.PROJECT.docs_url,
    openapi_url=APP_SETTINGS.PROJECT.openapi_url,
    redoc_url=APP_SETTINGS.PROJECT.redoc_url,
)
