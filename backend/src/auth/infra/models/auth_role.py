from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from src.core.database.base import Base
from src.core.database.mixins import TimestampMixin
from src.core.database.types import DefaultFalse, OptText, Str255, UniqueStr50

if TYPE_CHECKING:
    from .auth_permission import AuthPermissionORM
    from .user_role_assignment import UserRoleAssignmentORM


class AuthRoleORM(Base, TimestampMixin):
    """Auth role model."""

    name: Mapped[UniqueStr50]
    title: Mapped[Str255]
    description: Mapped[OptText]
    is_active: Mapped[DefaultFalse]

    users_assignments: Mapped[list["UserRoleAssignmentORM"]] = relationship(
        "UserRoleAssignmentORM",
        back_populates="role",
        uselist=True,
        cascade="all, delete-orphan",
    )

    permissions: Mapped[list["AuthPermissionORM"]] = relationship(
        secondary="association_role_permissions",
        back_populates="roles",
        uselist=True,
    )

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return (
            f"<AuthRole(name='{self.name}', "
            f"name='{self.name}', "
            f"title='{self.title}', "
            f"description='{self.description}', "
            f"is_active={self.is_active})>"
        )
