from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Annotated, Final

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..config import SERVER_SETTINGS as SETTINGS
from ..config import DatabaseSettings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio.engine import AsyncEngine


class DatabaseManager:
    """Database manager class."""

    def __init__(self, db_settings: DatabaseSettings) -> None:
        """Initialize the database."""
        self.async_engine: AsyncEngine = create_async_engine(
            url=str(db_settings.database_uri),
            echo=db_settings.echo,
            echo_pool=db_settings.echo_pool,
            pool_size=db_settings.pool_size,
            max_overflow=db_settings.max_overflow,
            pool_pre_ping=db_settings.pool_pre_ping,
            pool_recycle=db_settings.pool_recycle,
        )

        self.async_session_maker: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.async_engine,
                autoflush=db_settings.autoflush,
                autocommit=db_settings.autocommit,
                expire_on_commit=db_settings.expire_on_commit,
            )
        )

    async def dispose_engine(self) -> None:
        """Dispose the engine."""
        await self.async_engine.dispose()

    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        """Returns a database session."""
        async with self.async_session_maker() as session:
            yield session


DB_MANAGER: Final[DatabaseManager] = DatabaseManager(
    db_settings=SETTINGS.DATABASE
)

DBSessionDep = Annotated[AsyncSession, Depends(DB_MANAGER.get_session)]
