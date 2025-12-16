from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from src.core.database.base import Base
from src.core.database.mixins import TimestampMixin
from src.core.database.types import OptStr50, OptStr255, OptStr2048, OptText

from .types import UserIDForeignKey

if TYPE_CHECKING:
    from .user_orm import UserORM


class UserProfileORM(Base, TimestampMixin):
    """User profile model."""

    user_id: Mapped[UserIDForeignKey]
    first_name: Mapped[OptStr255]
    patronymic: Mapped[OptStr255]
    last_name: Mapped[OptStr255]
    bio: Mapped[OptText]
    avatar_url: Mapped[OptStr2048]
    timezone: Mapped[OptStr50]
    locale: Mapped[OptStr50]

    user: Mapped["UserORM"] = relationship(
        "UserORM", back_populates="profile", uselist=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", name="uq_userprofile_user_id"),
    )

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return (
            f"<UserProfile(id={self.id}, "
            f"user_id={self.user_id}, "
            f"patronymic={self.patronymic}, "
            f"first_name='{self.first_name}', "
            f"last_name='{self.last_name}', "
            f"timezone='{self.timezone}', "
            f"locale='{self.locale}')>"
        )
