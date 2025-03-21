import logging
import os
from logging.handlers import RotatingFileHandler

from constants import (DATETIME_FORMAT, LOG_FILE_PATH, LOG_FORMAT,
                       MAX_LOG_SIZE, MAX_LOGS_COUNT)


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
