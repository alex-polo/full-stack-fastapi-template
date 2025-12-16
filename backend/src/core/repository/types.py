from typing import TypeVar

from src.core.database.base import Base

TModel = TypeVar("TModel", bound=Base)
# TCreate = TypeVar("TCreate", bound=BaseModel)
# TUpdate = TypeVar("TUpdate", bound=BaseModel)
# TRead = TypeVar("TRead", bound=BaseModel)
