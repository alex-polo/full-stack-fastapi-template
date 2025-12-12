from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from src.core.database.base import Base
from src.core.database.mixins import TimestampMixin
from src.core.database.types import DefaultFalse, UniqueEmailStr

from .types import HashedPassword

if TYPE_CHECKING:
    from .user_profile_orm import UserProfileORM
    from .user_role_assignment import UserRoleAssignmentORM


class UserORM(Base, TimestampMixin):
    """User model."""

    email: Mapped[UniqueEmailStr]
    hashed_password: Mapped[HashedPassword]
    is_active: Mapped[DefaultFalse]
    is_superuser: Mapped[DefaultFalse]
    is_verified: Mapped[DefaultFalse]

    profile: Mapped["UserProfileORM"] = relationship(
        "UserProfileORM",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select",
    )

    roles_assignments: Mapped[list["UserRoleAssignmentORM"]] = relationship(
        "UserRoleAssignmentORM",
        back_populates="user",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return (
            f"<User(email='{self.email}', "
            f"email={self.email}, "
            f"is_active={self.is_active}, "
            f"is_superuser={self.is_superuser}, "
            f"is_verified={self.is_verified})>"
        )
