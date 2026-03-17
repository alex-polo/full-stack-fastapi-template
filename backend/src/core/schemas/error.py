from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Detailed error information."""

    code: str = Field(..., description="Status code")
    message: str = Field(..., description="Message describing the error")
    path: str = Field(..., description="Path of the request")
    details: dict[str, Any] | None = None


class ErrorSchema(BaseModel):
    """Error schema for OpenAPI."""

    error: ErrorDetail
