"""Конфигурация объекта drivermanager и телеграм бота."""
import os
import platform

from bot_classes import DriverManager
from constants import (LINUX_PROFILE_DIR, TELEGRAM_BOT_TOKEN,
                       WINDOWS_PROFILE_DIR)
from telebot import TeleBot

manager = DriverManager(
    bot=TeleBot(token=TELEGRAM_BOT_TOKEN)
)

if platform.system() == 'Windows':
    profile_dir = os.path.join(os.getcwd(), WINDOWS_PROFILE_DIR)
else:
    profile_dir = os.path.join(os.getcwd(), LINUX_PROFILE_DIR)

os.makedirs(profile_dir, exist_ok=True)

manager.options.add_argument('--start-maximized')
manager.options.add_argument(f"user-data-dir={profile_dir}")
manager.options.add_argument('--ignore-certificate-errors')
manager.options.add_experimental_option(
    "excludeSwitches", ["enable-automation"]
)
manager.options.add_experimental_option('useAutomationExtension', False)
