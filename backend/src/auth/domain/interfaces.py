from abc import ABC, abstractmethod

from .entities.user import User


class IUserRepository(ABC):
    """User repository."""

    @abstractmethod
    async def add_user(self, user: User) -> User: ...  # noqa: D102

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...  # noqa: D102

    @abstractmethod
    async def get_by_id(self, id: int) -> User | None: ...  # noqa: D102

    # @abstractmethod
    # async def save(self, user: User) -> None: ...
