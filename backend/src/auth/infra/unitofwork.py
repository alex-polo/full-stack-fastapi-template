from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.infra.repositories.user_repository import SQLAUserRepository
from src.core.database.unitofwork import SQLAUnitOfWork


class AuthUnitOfWork(SQLAUnitOfWork):
    """Auth unit of work."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the auth unit of work."""
        super().__init__(session)
        self.user_repo = SQLAUserRepository(session)
        self.profile_repo = SQLAUserRepository(session)


_all__ = ["AuthUnitOfWork"]
