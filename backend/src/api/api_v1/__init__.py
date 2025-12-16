from fastapi import APIRouter

from src.auth.api.routes import router as auth_router
from src.core.config import SERVER_SETTINGS

router = APIRouter(
    prefix=SERVER_SETTINGS.API_PREFIX.v1.prefix,
)


router.include_router(
    auth_router,
    prefix=SERVER_SETTINGS.AUTH.prefix,
    tags=[
        "Auth",
    ],
)
