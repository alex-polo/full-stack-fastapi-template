from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.core.config import APP_SETTINGS

api_v1_router = APIRouter(
    prefix=APP_SETTINGS.API_PREFIX.v1.prefix,
)


@api_v1_router.get("/health")
async def health_check() -> JSONResponse:
    """Health check."""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy"},
    )
