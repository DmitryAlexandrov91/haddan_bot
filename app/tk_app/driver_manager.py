"""Конфигурация объекта drivermanager и телеграм бота."""
import os
import platform

from bot_classes import HaddanDriverManager
from constants import (LINUX_PROFILE_DIR, TELEGRAM_BOT_TOKEN,
                       WINDOWS_PROFILE_DIR)
from telebot import TeleBot

if TELEGRAM_BOT_TOKEN:
    manager = HaddanDriverManager(
        bot=TeleBot(token=TELEGRAM_BOT_TOKEN)
    )
else:
    manager = HaddanDriverManager()


if platform.system() == 'Windows':
    profile_dir = os.path.join(os.getcwd(), WINDOWS_PROFILE_DIR)
else:
    profile_dir = os.path.join(os.getcwd(), LINUX_PROFILE_DIR)

os.makedirs(profile_dir, exist_ok=True)

#  Сохраняет куки/сессии
manager.options.add_argument(f'user-data-dir={profile_dir}')
#  Игнорирует SSL-ошибки
manager.options.add_argument('--ignore-certificate-errors')

# Разрешает смешанный контент
manager.options.add_argument('--allow-running-insecure-content')
