import os
import sys
from pathlib import Path

from constants import Slot, SlotsPage
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс базовых настроек приложения."""

    TELEGRAM_BOT_TOKEN: str = ''
    TELEGRAM_CHAT_ID: str = ''
    FIRST_CHAR: str = ''
    SECOND_CHAR: str = ''
    THIRD_CHAR: str = ''
    HADDAN_PASSWORD: str = ''

    MIN_HP_VALUE: str = '0'
    MIND_SPIRIT_PLAY: bool = True
    CHEERFULNESS: bool = False
    DEFAULT_SLOTS_PAGE: str = SlotsPage._1
    DEFAULT_SLOT: str = Slot._1
    DEFAULT_CHEERFULNESS_SLOTS_PAGE: str = SlotsPage._0
    DEFAULT_CHEERFULNESS_SLOT: str = Slot._1
    DEFAULT_CHEERFULNESS_MIN: int = 96

    BEETS_DELAY: int | float = 0.2
    PAGE_LOAD_TIMEOUT: int = 2
    SCRIPT_TIMEOUT: int = 1

    MIN_TO_RElOAD: int = 15
    MIN_TO_REFRESH: int = 5

    WINDOWS_PROFILE_DIR: str = 'hd_windows_profile'
    LINUX_PROFILE_DIR: str = 'hd_linux_profile'

    BASE_DIR: Path = Path(sys.executable).parent if getattr(
        sys, 'frozen', False,
    ) else Path(__file__).resolve().parent.parent

    data_dir: Path = BASE_DIR / 'data'
    if not data_dir.exists():
        data_dir.mkdir()

    DB_URL: str = f"sqlite:///{BASE_DIR}/data/db.sqlite3"

    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def chars_list(self) -> list[str]:
        """Формирует список всех персонажей."""
        return [
            self.FIRST_CHAR,
            self.SECOND_CHAR,
            self.THIRD_CHAR,
        ]


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
