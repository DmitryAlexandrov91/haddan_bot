import logging
import os
import sys
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
    """Класс базовых настроек приложения."""

    BASE_DIR: Path = Path(sys.executable).parent if getattr(
        sys, 'frozen', False,
    ) else Path(__file__).resolve().parent.parent

    data_dir: Path = BASE_DIR / 'data'
    if not data_dir.exists():
        data_dir.mkdir()

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
