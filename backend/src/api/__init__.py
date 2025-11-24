from fastapi import APIRouter

from src.core.config.constants import SERVER_SETTINGS

from .api_v1 import router as api_v1_router

api_router = APIRouter()

api_router.include_router(
    api_v1_router, prefix=SERVER_SETTINGS.API_PREFIX.v1.prefix, tags=["v1"]
)
