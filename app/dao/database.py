import uuid
from datetime import datetime
from decimal import Decimal


from config import database_url
from sqlalchemy import Boolean, Identity, Integer, create_engine, inspect

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    sessionmaker,
)


sync_engine = create_engine(url=database_url)
sync_session_maker = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class BaseModel(DeclarativeBase):
    """Базовый класс для всех моделей."""

    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()

    id: Mapped[int] = mapped_column(
            Integer,
            Identity(always=True),
            primary_key=True,
        )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def to_dict(self, exclude_none: bool = False) -> dict:
        """Преобразует объект модели в словарь.

        Args:
            exclude_none (bool): Исключать ли None значения из результата

        Returns:
            dict: Словарь с данными объекта

        """
        result = {}
        for column in inspect(self.__class__).columns:
            value = getattr(self, column.key)

            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, uuid.UUID):
                value = str(value)

            if not exclude_none or value is not None:
                result[column.key] = value

        return result
