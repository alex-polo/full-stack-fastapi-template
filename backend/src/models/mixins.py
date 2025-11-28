from .types import CreatedAt, IntPk, UpdatedAt


class IntIdMixin:
    """Mixin for models with an integer primary key."""

    id: IntPk


class TimestampMixin:
    """Mixin for models with a created_at and updated_at columns."""

    created_at: CreatedAt
    updated_at: UpdatedAt
