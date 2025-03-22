"""Бот python-скриптом."""
import os
from time import sleep  # noqa

from bot_classes import DriverManager, HaddanBot
from constants import FIRST_CHAR, PASSWORD, SECOND_CHAR  # noqa

if __name__ == '__main__':
    manager = DriverManager()
    manager.options.add_argument('--start-maximized')
    profile_dir = os.path.join(os.getcwd(), 'haddan_tk_profile')
    os.makedirs(profile_dir, exist_ok=True)
    manager.options.add_argument(f"user-data-dir={profile_dir}")
    manager.start_driver()

    user = HaddanBot(
        char=FIRST_CHAR,
        password=PASSWORD,
        driver=manager.driver)
    user.login_to_game()

    manager.glade_farm()
