from typing import Annotated

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column

UserIDForeignKey = Annotated[
    int,
    mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True),
]
RoleIDForeignKey = Annotated[
    int,
    mapped_column(ForeignKey("auth_roles.id", ondelete="CASCADE"), index=True),
]
HashedPassword = Annotated[
    str,
    mapped_column(String(length=128)),
]
