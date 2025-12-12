from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession


class BaseUnitOfWork(ABC):
    """Abstract base class for Unit of Work pattern.

    Coordinates transaction management across repositories.
    Subclasses must implement commit and rollback logic.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize Unit of Work with database session.

        Args:
            session: Async database session.
        """
        self._session = session

    async def __aenter__(self) -> Self:
        """Enter async context manager.

        Returns:
            Self instance for use in async with statement.
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager.

        Commits transaction if no exception occurred,
        otherwise rolls back.

        Args:
            exc_type: Exception type or None.
            exc_val: Exception instance or None.
            exc_tb: Traceback or None.
        """
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Roll back the current transaction."""
        ...


class SQLAUnitOfWork(BaseUnitOfWork):
    """SQLAlchemy implementation of Unit of Work."""

    async def commit(self) -> None:
        """Commit the current transaction."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Roll back the current transaction."""
        await self._session.rollback()
