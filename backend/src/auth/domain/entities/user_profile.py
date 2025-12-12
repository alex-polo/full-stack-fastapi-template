from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserProfile:
    """User profile entity."""

    id: int | None = None
    user_id: int | None = None
    first_name: str | None = None
    patronymic: str | None = None
    last_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    timezone: str | None = None
    locale: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return (
            f"<UserProfile(id={self.id}, "
            f"first_name='{self.first_name}', "
            f"patronymic='{self.patronymic}', "
            f"last_name='{self.last_name}', "
            f"bio='{self.bio}', "
            f"avatar_url='{self.avatar_url}', "
            f"timezone='{self.timezone}', "
            f"locale='{self.locale}', "
            f"created_at='{self.created_at}', "
            f"updated_at='{self.updated_at}')>"
        )
