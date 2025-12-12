from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.auth.domain.entities.user import User
from src.auth.domain.entities.user_profile import UserProfile
from src.auth.domain.interfaces import IUserRepository
from src.auth.infra.models.user_orm import UserORM
from src.auth.infra.models.user_profile_orm import UserProfileORM
from src.core.repository.sqla import SQLAlchemyRepository


class SQLAUserRepository(IUserRepository, SQLAlchemyRepository[UserORM]):
    """User repository."""

    model = UserORM

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the user repository."""
        self.session: AsyncSession = session

    async def add_user(self, user: User) -> User:
        """Add user."""
        user_orm: UserORM = self._to_orm(user=user)
        self.session.add(user_orm)
        await self.session.flush()

        return self._to_domain(user_orm=user_orm)

    async def get_by_id(self, id: int) -> User | None:
        """Get user by email."""
        stmt = (
            select(self.model)
            .options(joinedload(self.model.profile))
            .where(self.model.id == id)
        )

        user_orm: UserORM | None = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        if user_orm is None:
            return None

        return self._to_domain(user_orm=user_orm)

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        user_orm: UserORM | None = await self.session.scalar(
            select(self.model)
            .where(
                self.model.email == email,
            )
            .options(joinedload(self.model.profile))
        )

        if user_orm is None:
            return None

        return self._to_domain(user_orm=user_orm)

    def _to_orm(self, user: User) -> UserORM:
        return UserORM(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            profile=(
                None
                if user.profile is None
                else self._to_orm_profile(user.profile)
            ),
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            is_verified=user.is_verified,
        )

    def _to_orm_profile(self, user_profile: UserProfile) -> UserProfileORM:
        return UserProfileORM(
            first_name=user_profile.first_name,
            patronymic=user_profile.patronymic,
            last_name=user_profile.last_name,
            bio=user_profile.bio,
            avatar_url=user_profile.avatar_url,
            timezone=user_profile.timezone,
            locale=user_profile.locale,
        )

    def _to_domain_profile(self, user_profile: UserProfileORM) -> UserProfile:

        return UserProfile(
            id=user_profile.id,
            user_id=user_profile.user_id,
            first_name=user_profile.first_name,
            patronymic=user_profile.patronymic,
            last_name=user_profile.last_name,
            bio=user_profile.bio,
            avatar_url=user_profile.avatar_url,
            timezone=user_profile.timezone,
            locale=user_profile.locale,
            created_at=user_profile.created_at,
            updated_at=user_profile.updated_at,
        )

    def _to_domain(self, user_orm: UserORM) -> User:
        """Convert ORM model to domain model."""
        return User(
            id=user_orm.id,
            email=user_orm.email,
            hashed_password=user_orm.hashed_password,
            profile=self._to_domain_profile(user_profile=user_orm.profile),
            is_active=user_orm.is_active,
            is_superuser=user_orm.is_superuser,
            is_verified=user_orm.is_verified,
        )
