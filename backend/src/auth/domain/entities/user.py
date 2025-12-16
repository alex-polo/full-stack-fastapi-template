from dataclasses import dataclass
from datetime import datetime

from src.auth.domain.entities.user_profile import UserProfile


@dataclass
class User:
    """User entity."""

    email: str
    id: int | None = None
    hashed_password: str | None = None
    profile: UserProfile | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    is_verified: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return (
            f"<User(email='{self.email}', "
            f"id={self.id}, "
            f"profile='{self.profile}', "
            f"is_active={self.is_active}, "
            f"is_superuser={self.is_superuser}, "
            f"is_verified={self.is_verified}, "
            f"created_at='{self.created_at}', "
            f"updated_at='{self.updated_at}')>"
        )
