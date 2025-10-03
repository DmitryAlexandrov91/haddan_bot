from dataclasses import dataclass

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


@dataclass
class SessionService:
    """Класс для регистрации сервиса сессий в DI."""

    _engine: Engine

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
        """Позволяет использовать SessionService как фабрику сессий."""
        return self.session()
