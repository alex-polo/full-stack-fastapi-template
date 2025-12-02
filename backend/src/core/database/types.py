from datetime import UTC, datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import mapped_column

from src.core.utils import utcnow

__all__ = ["CreatedAt", "IntPk", "UpdatedAt"]


IntPk = Annotated[int, mapped_column(primary_key=True)]

CreatedAt = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        default=utcnow,
        server_default=func.now(),
    ),
]

UpdatedAt = Annotated[
    datetime,
    mapped_column(
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
        server_default=func.now(),
    ),
]
