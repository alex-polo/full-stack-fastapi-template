import contextlib
import logging
from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_roter
from src.core.config import APP_SETTINGS
from src.core.database.engine import DB_HANDLER

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from fastapi.routing import APIRoute

log = logging.getLogger(__name__)


def custom_generate_unique_id(route: APIRoute) -> str:
    """Generate unique id for OpenAPI route."""
    return f"{route.tags[0]}-{route.name}"


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
    generate_unique_id_function=custom_generate_unique_id,
)


app.include_router(api_roter)


app.add_middleware(
    CORSMiddleware,
    allow_origins=APP_SETTINGS.CORS.allow_origins,
    allow_credentials=APP_SETTINGS.CORS.allow_credentials,
    allow_methods=APP_SETTINGS.CORS.allow_methods,
    allow_headers=APP_SETTINGS.CORS.allow_headers,
)
