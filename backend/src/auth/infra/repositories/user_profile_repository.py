from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.domain.interfaces import IUserRepository
from src.auth.infra.models.user_profile_orm import UserProfileORM
from src.core.repository.sqla import SQLAlchemyRepository


class SQLAUserProfileRepository(
    IUserRepository, SQLAlchemyRepository[UserProfileORM]
):
    """User repository."""

    model = UserProfileORM

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the user repository."""
        self.session: AsyncSession = session
