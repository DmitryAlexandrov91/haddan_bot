from typing import final

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


@final
class SessionService:
    """Класс для регистрации сервиса сессий в DI."""

    def __init__(self, engine: Engine) -> None:
        """Инициализация движка из контейнера."""
        self._engine = engine

    @property
    def session(self) -> sessionmaker[Session]:
        """Возвращает сессию."""
        return sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    def __call__(self) -> Session:
        """Позволяет использовать SessionService() как фабрику сессий."""
        return self.session()
