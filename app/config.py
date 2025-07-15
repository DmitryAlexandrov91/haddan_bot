import logging
import os
from logging.handlers import RotatingFileHandler

from pydantic_settings import BaseSettings

from constants import (DATETIME_FORMAT, LOG_FILE_PATH, LOG_FORMAT,
                           MAX_LOG_SIZE, MAX_LOGS_COUNT)


class Settings(BaseSettings):
    BASE_DIR: str = os.getcwd()
    DB_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/data/db.sqlite3"


def configure_logging():
    logs_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOG_FILE_PATH,
        maxBytes=MAX_LOG_SIZE,
        backupCount=MAX_LOGS_COUNT,
        encoding='utf-8'
    )
    logging.basicConfig(
        datefmt=DATETIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler()),
    )


settings = Settings()
database_url = settings.DB_URL
