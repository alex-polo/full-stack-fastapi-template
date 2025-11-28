from datetime import UTC, datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.utils import utcnow

IntPk = Annotated[Mapped[int], mapped_column(primary_key=True)]
IntPkOptional = Annotated[
    Mapped[int], mapped_column(primary_key=True, nullable=True)
]

CreatedAt = Annotated[
    Mapped[datetime],
    mapped_column(
        TIMESTAMP(timezone=True),
        default=utcnow,
        server_default=func.now(),
    ),
]

UpdatedAt = Annotated[
    Mapped[datetime],
    mapped_column(
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
        server_default=func.now(),
    ),
]
