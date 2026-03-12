import contextlib
import logging
from typing import TYPE_CHECKING

from fastapi import FastAPI

from src.api import api_roter
from src.core.config import APP_SETTINGS
from src.core.database.engine import DB_HANDLER

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

log = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    """FastAPI lifespan context manager."""
    try:
        yield
    finally:
        await DB_HANDLER.dispose_engine()


app = FastAPI(
    title=APP_SETTINGS.PROJECT.title,
    description=APP_SETTINGS.PROJECT.description,
    docs_url=APP_SETTINGS.PROJECT.docs_url,
    openapi_url=APP_SETTINGS.PROJECT.openapi_url,
    redoc_url=APP_SETTINGS.PROJECT.redoc_url,
    lifespan=lifespan,
)


app.include_router(api_roter)
