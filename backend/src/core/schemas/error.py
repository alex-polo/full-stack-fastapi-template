from pydantic import BaseModel, ConfigDict, Field


class ErrorDetail(BaseModel):
    """Detailed error information."""

    code: str = Field(..., description="Status code")
    message: str = Field(..., description="Message describing the error")
    path: str = Field(..., description="Path of the request")


class ErrorSchema(BaseModel):
    """Error schema for OpenAPI."""

    error: ErrorDetail

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "code": "ENTITY_NOT_FOUND",
                    "message": "Entity not found",
                    "path": "/api/v1/entity/{entity_id}",
                }
            }
        }
    )
