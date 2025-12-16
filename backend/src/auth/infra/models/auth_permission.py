from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from src.core.database.base import Base
from src.core.database.mixins import TimestampMixin
from src.core.database.types import DefaultFalse, OptText, Str255, UniqueStr50

if TYPE_CHECKING:
    from .auth_role import AuthRoleORM


class AuthPermissionORM(Base, TimestampMixin):
    """Auth permission model."""

    name: Mapped[UniqueStr50]
    title: Mapped[Str255]
    description: Mapped[OptText]
    is_active: Mapped[DefaultFalse]

    roles: Mapped[list["AuthRoleORM"]] = relationship(
        secondary="association_role_permissions",
        back_populates="permissions",
    )

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return (
            f"<AuthPermission(name='{self.name}', "
            f"name='{self.name}', "
            f"title='{self.title}', "
            f"description='{self.description}', "
            f"is_active={self.is_active})>"
        )
