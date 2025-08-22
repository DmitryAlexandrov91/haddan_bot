import os
import sys
from pathlib import Path

from loguru import logger
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

    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"


settings = Settings()

database_url = settings.DB_URL


def configure_logging() -> None:
    """Концигурация loguru."""
    log_file_path = os.path.join(
        settings.BASE_DIR, "log.txt")
    logger.add(
        log_file_path,
        format=settings.FORMAT_LOG,
        level="INFO",
        rotation=settings.LOG_ROTATION)
