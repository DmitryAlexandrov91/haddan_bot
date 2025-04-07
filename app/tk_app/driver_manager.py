"""Конфигурация объекта drivermanager и тегерам бота."""
import os

from bot_classes import DriverManager
from constants import TELEGRAM_BOT_TOKEN
from telebot import TeleBot

manager = DriverManager(
    bot=TeleBot(token=TELEGRAM_BOT_TOKEN)
)
manager.options.add_argument('--start-maximized')
profile_dir = os.path.join(os.getcwd(), 'haddan_tk_profile')
os.makedirs(profile_dir, exist_ok=True)
manager.options.add_argument(f"user-data-dir={profile_dir}")
manager.options.add_argument('--ignore-certificate-errors')
manager.options.add_experimental_option(
    "excludeSwitches", ["enable-automation"]
)
manager.options.add_experimental_option('useAutomationExtension', False)
