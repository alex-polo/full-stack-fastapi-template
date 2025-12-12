from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from src.core.database.base import Base
from src.core.database.mixins import TimestampMixin
from src.core.database.types import OptStr20, OptStr255

from .types import RoleIDForeignKey, UserIDForeignKey

if TYPE_CHECKING:
    from .auth_role import AuthRoleORM
    from .user_orm import UserORM


class UserRoleAssignmentORM(Base, TimestampMixin):
    """User role relation model."""

    user_id: Mapped[UserIDForeignKey]
    role_id: Mapped[RoleIDForeignKey]
    source: Mapped[OptStr20]
    reason: Mapped[OptStr255]

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )

    user: Mapped["UserORM"] = relationship(
        "UserORM",
        back_populates="roles_assignments",
        uselist=False,
        lazy="select",
    )
    role: Mapped["AuthRoleORM"] = relationship(
        "AuthRoleORM",
        back_populates="users_assignments",
        uselist=False,
        lazy="select",
    )

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return (
            f"<UserRoleAssignment(user_id={self.user_id}, "
            f"role_id={self.role_id})>"
        )
