import contextlib
from collections.abc import AsyncIterator

from fastapi import FastAPI

from src.core.config.logging import setup_logging
from src.core.database import DB_MANAGER

from .api import api_router
from .core.config import SERVER_SETTINGS as SETTINGS

setup_logging()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    """FastAPI lifespan context manager."""
    yield
    await DB_MANAGER.dispose_engine()


app = FastAPI(
    title=SETTINGS.PROJECT.project_name,
    description=SETTINGS.PROJECT.description,
    docs_url=SETTINGS.PROJECT.docs_url,
    openapi_url=SETTINGS.PROJECT.openapi_url,
    redoc_url=SETTINGS.PROJECT.redoc_url,
    lifespan=lifespan,
)


app.include_router(api_router)
