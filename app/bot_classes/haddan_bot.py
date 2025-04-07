from constants import HADDAN_MAIN_URL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telebot import TeleBot


class HaddanBot:

    """Бот класс управления действиями персонажа.

    Принимает два обязательных аргумента при инициализации:
        char - никнейм персонажа,
        driver - объект класса webdriver.Chrome.

    """

    def __init__(self, char, driver, password, bot=None):
        self.driver: webdriver.Chrome = driver
        self.char: str = char
        self.password: str = password
        self.bot: TeleBot = bot
        self.login_url: str = HADDAN_MAIN_URL

    def login_to_game(self):
        """Заходит в игру под заданным именем char."""
        self.driver.get(self.login_url)
        username_field = self.driver.find_element(
            By.NAME, 'username')
        username_field.send_keys(self.char)
        password_field = self.driver.find_element(
            By.NAME, 'passwd')
        password_field.send_keys(self.password)
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR,
            '[href="javascript:enterHaddan()"]')
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                submit_button)
            )
        submit_button.click()
