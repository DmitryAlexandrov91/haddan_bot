
"""Всё что связано с конкретным игроком."""
from constants import (
    HADDAN_URL,
)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class HaddanUser:

    """Бот класс управления действиями персонажа.

    Принимает два обязательных аргумента при инициализации:
    :char: никнейм персонажа,
    :driver: объект класса webdriver.Chrome.

    """

    def __init__(
            self,
            char: str,
            driver: webdriver.Chrome,
            password: str,
    ) -> None:
        """Инициализация класса HaddanUser."""
        self.driver = driver
        self.char = char
        self.password = password
        self.login_url: str = HADDAN_URL

    def login_to_game(self, domen: str) -> None:
        """Заходит в игру под заданным именем char."""
        try:
            self.driver.get(domen)
            username_field = self.driver.find_element(
                By.NAME, 'username')
            username_field.send_keys(self.char)
            password_field = self.driver.find_element(
                By.NAME, 'passwd')
            password_field.send_keys(self.password)
            submit_button = self.driver.find_element(
                By.CSS_SELECTOR,
                '[href="javascript:void(enterHaddan())"]')
            WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(
                    submit_button),
                )
        except Exception:
            self.login_to_game(domen=domen)
        finally:
            submit_button.click()

    def exit_from_game(self) -> None:
        """Выходит из игры."""
        exit_button = self.driver.find_elements(
            By.CSS_SELECTOR,
            'img[alt="ВЫХОД"]',
        )
        if exit_button:
            exit_button[0].click()
