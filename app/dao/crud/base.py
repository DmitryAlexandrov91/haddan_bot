from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from dao.database import BaseModel

T = TypeVar('T', bound='BaseModel')


class BaseCRUD(Generic[T]):
    """Базовый CRUD класс с общими операциями."""

    def __init__(self, model: Type[T]) -> None:
        """Инициализация базового CRUD."""
        self.model = model

    def get(self, session: Session, obj_id: int) -> Optional[T]:
        """Получение записи по ID."""
        return session.get(self.model, obj_id)

    def get_single_filtered(
        self,
        session: Session,
        **filters: Any,
    ) -> T | None:
        """Возвращает последнюю добавленную запись по параметру."""
        return (session.query(self.model).filter_by(**filters).order_by(
            self.model.id.desc(),
            ).first()
        )

    def get_multi(
        self,
        session: Session,
    ) -> List[T]:
        """Получение всех записей."""
        return session.query(self.model).all()

    def get_multi_filtered(
            self,
            session: Session,
            **filters: Any) -> Optional[List[T]]:
        """Получение всех записей с фильтрами."""
        return (session.query(self.model).filter_by(**filters)).all()

    def create(self, session: Session, **kwargs: Any) -> T:
        """Создание новой записи."""
        instance = self.model(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    def get_or_create_or_update(self, session: Session, **kwargs: Any) -> T:
        """Получает, обновляет, создаёт объект в БД."""
        filter_kwargs = kwargs
        if hasattr(self.model, 'name'):
            filter_kwargs = {'name': kwargs.get('name')}

        obj = session.query(self.model).filter_by(**filter_kwargs).first()
        if obj:
            for key, value in kwargs.items():
                if hasattr(obj, key) and getattr(obj, key) != value:
                    setattr(obj, key, value)
            session.commit()
            session.refresh(obj)
        else:
            obj = self.model(**kwargs)
            session.add(obj)
            session.commit()
            session.refresh(obj)
        return obj
