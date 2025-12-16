from sqlalchemy import Column, ForeignKey, Table

from src.core.database.base import Base

association_role_permissions = Table(
    "association_role_permissions",
    Base.metadata,
    Column(
        "role_id",
        ForeignKey("auth_roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        ForeignKey("auth_permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
