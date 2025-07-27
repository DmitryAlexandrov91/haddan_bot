import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from constants import (
    DATETIME_FORMAT,
    LOG_FILE_PATH,
    LOG_FORMAT,
    MAX_LOGS_COUNT,
    MAX_LOG_SIZE,
)
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс базовых настроект приложения."""

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DB_URL: str = f"sqlite:///{BASE_DIR}/data/db.sqlite3"


settings = Settings()
database_url = settings.DB_URL


def configure_logging() -> None:
    """Конфигурация логгера."""
    logs_dir = os.path.join(settings.BASE_DIR, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOG_FILE_PATH,
        maxBytes=MAX_LOG_SIZE,
        backupCount=MAX_LOGS_COUNT,
        encoding='utf-8',
    )
    logging.basicConfig(
        datefmt=DATETIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler()),
    )
