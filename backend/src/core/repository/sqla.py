from typing import Any

from sqlalchemy import delete, insert, select, update

from src.core.repository.base import BaseRepository
from src.core.repository.types import TModel


class SQLAlchemyRepository(BaseRepository[TModel]):
    """Generic SQLAlchemy repository implementation.

    Subclasses must define:
        model: SQLAlchemy ORM model class
    """

    model: type[TModel]

    async def _add_core(self, data: dict[str, Any]) -> TModel:
        """Create a new record in the database.

        Args:
            data: Dictionary of field values to insert.

        Returns:
            Created ORM model instance.
        """
        stmt = insert(self.model).values(**data).returning(self.model)
        created_entity: TModel = (
            await self.session.execute(stmt)
        ).scalar_one()
        return created_entity

    async def _add_many_core(self, data: list[dict[str, Any]]) -> list[TModel]:
        """Create multiple records in the database.

        Args:
            data: List of dictionaries with field values to insert.

        Returns:
            List of created ORM model instances.
        """
        stmt = insert(self.model).values(data).returning(self.model)
        created_entities = (await self.session.execute(stmt)).scalars().all()
        return list(created_entities)

    async def _get_by_id_core(self, id: int) -> TModel | None:
        """Retrieve a single record by ID.

        Args:
            id: Record identifier.

        Returns:
            ORM model instance, or None if not found.
        """
        # entity: TModel | None = await self.session.scalar(
        #     select(self.model).where(self.model.id == id)
        # )
        entity = await self.session.get(self.model, id)
        return entity

    async def _get_by_ids_core(self, ids: list[int]) -> list[TModel]:
        """Retrieve multiple records by IDs.

        Args:
            ids: List of record identifiers.

        Returns:
            List of found ORM model instances (missing IDs are omitted).
        """
        stmt = select(self.model).where(self.model.id.in_(ids))
        entities = (await self.session.execute(stmt)).scalars().all()
        return list(entities)

    async def _get_all_core(
        self, offset: int = 0, limit: int = 100
    ) -> list[TModel]:
        """Retrieve paginated records.

        Args:
            offset: Number of records to skip.
            limit: Maximum number of records to return (capped at 1000).

        Returns:
            List of ORM model instances.
        """
        safe_limit = max(1, min(limit, 1000))
        stmt = select(self.model).offset(offset).limit(safe_limit)
        entities = (await self.session.execute(stmt)).scalars().all()
        return list(entities)

    async def _update_core(
        self, id: int, data: dict[str, Any]
    ) -> TModel | None:
        """Update a record by ID.

        Args:
            id: Record identifier.
            data: Dictionary of field values to update.

        Returns:
            Updated ORM model instance, or None if not found.
        """
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        updated_entity: TModel | None = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()
        return updated_entity

    async def _delete_core(self, id: int) -> int | None:
        """Delete a record by ID.

        Args:
            id: Record identifier.

        Returns:
            Deleted record ID, or None if not found.
        """
        stmt = (
            delete(self.model)
            .where(self.model.id == id)
            .returning(self.model.id)
        )
        deleted_id: int | None = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()
        return deleted_id

    async def _delete_many_core(self, ids: list[int]) -> list[int]:
        """Delete multiple records by IDs.

        Args:
            ids: List of record identifiers.

        Returns:
            List of successfully deleted record IDs.
        """
        stmt = (
            delete(self.model)
            .where(self.model.id.in_(ids))
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        deleted_ids = result.scalars().all()
        return list(deleted_ids)
