from dataclasses import dataclass

from dao.services import SessionService
from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy import Engine


@dataclass
class AdminService:
    """"Сервис для создания объекта для админки SQLAdmin."""

    _app: FastAPI
    _engine: Engine
    _session_service: SessionService

    def __call__(self) -> Admin:
        """Создаёт объект Admin."""
        return Admin(
            self._app,
            engine=self._engine,
            session_maker=self._session_service.session,
        )
