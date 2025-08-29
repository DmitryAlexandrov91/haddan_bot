"""Конфигурация объекта drivermanager и телеграм бота."""
import os
import platform

from aiogram import Bot
from bot_classes import HaddanDriverManager
from config import settings
from di import resolve

if settings.TELEGRAM_BOT_TOKEN:
    manager = HaddanDriverManager(
        bot=resolve(Bot),
    )
else:
    manager = HaddanDriverManager()


if platform.system() == 'Windows':
    profile_dir = os.path.join(
        os.getcwd(),
        settings.WINDOWS_PROFILE_DIR,
    )
else:
    profile_dir = os.path.join(
        os.getcwd(),
        settings.LINUX_PROFILE_DIR,
    )

os.makedirs(profile_dir, exist_ok=True)

#  Сохраняет куки/сессии
manager.options.add_argument(f'user-data-dir={profile_dir}')
#  Игнорирует SSL-ошибки
manager.options.add_argument('--ignore-certificate-errors')

# Разрешает смешанный контент
manager.options.add_argument('--allow-running-insecure-content')
