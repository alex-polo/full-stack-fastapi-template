from fastapi import APIRouter

from src.core.config import APP_SETTINGS

from .api_v1 import api_v1_router

api_roter = APIRouter(prefix=APP_SETTINGS.API_PREFIX.prefix)

api_roter.include_router(api_v1_router)

__all__ = ("api_roter",)
