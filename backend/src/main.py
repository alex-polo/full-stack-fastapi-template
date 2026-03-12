import contextlib
import logging
from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.api import api_router
from src.core.config import APP_SETTINGS
from src.core.config.logging import setup_logging
from src.core.database import DB_HANDLER

from .middleware import logging_middleware, request_id_middleware, timing_middleware

# Инициализация логирования (должна быть ПЕРЕД созданием app)
setup_logging()

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

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=APP_SETTINGS.CORS.allow_origins,
    allow_credentials=APP_SETTINGS.CORS.allow_credentials,
    allow_methods=APP_SETTINGS.CORS.allow_methods,
    allow_headers=APP_SETTINGS.CORS.allow_headers,
)

if APP_SETTINGS.ENVIRONMENT in ("production", "staging"):
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            APP_SETTINGS.DOMAIN,
            f"www.{APP_SETTINGS.DOMAIN}",
        ],
    )


app.middleware("http")(request_id_middleware)
app.middleware("http")(timing_middleware)
app.middleware("http")(logging_middleware)


app.add_middleware(GZipMiddleware, minimum_size=1000)
