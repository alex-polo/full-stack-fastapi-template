from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[TModel]:
    """Base repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Base repository."""
        self.session = session

    # @abstractmethod
    # async def add(self, data: dict) -> TRead:
    #     """Create a new record."""
    #     ...

    # @abstractmethod
    # async def get_by_id(self, id: int) -> TRead:
    #     """Get a record by id."""
    #     ...

    # @abstractmethod
    # async def update(self, id: int, data: TUpdate) -> TRead:
    #     """Update a record."""
    #     ...

    # @abstractmethod
    # async def delete(self, id: int) -> int:
    #     """Delete a record."""
    #     ...
