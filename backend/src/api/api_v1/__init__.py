from fastapi import APIRouter

from src.core.config import SERVER_SETTINGS

router = APIRouter(prefix=SERVER_SETTINGS.API_PREFIX.prefix)
