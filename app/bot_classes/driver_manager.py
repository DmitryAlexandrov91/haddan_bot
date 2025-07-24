import logging
import platform
import re
import threading
import tkinter as tk
from time import sleep
from typing import Optional

import undetected_chromedriver as uc
from aiogram import Bot
from config import configure_logging
from constants import CHROME_PATH
from selenium import webdriver
from selenium.common.exceptions import (
    InvalidSessionIdException,
    NoAlertPresentException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    """Класс создания и управления объектом webdriver.Chrome."""

    def __init__(
            self,
            bot: Optional[Bot] = None,
            driver: Optional[webdriver.Chrome] = None,
            cycle_thread: Optional[threading.Thread] = None,
            event: threading.Event = threading.Event(),
            errors_count: int = 0,
            wait_timeout: int = 30,
            alarm_label: Optional[tk.Label] = None,
            info_label: Optional[tk.Label] = None,
            status_label: Optional[tk.Label] = None,
            start_button: Optional[tk.Button] = None,
            forest_button: Optional[tk.Button] = None,
    ) -> None:
        """Инициализация класса DriverManager."""
        self.options = self._get_default_options()
        self.driver = driver
        self.cycle_thread = cycle_thread
        self.bot = bot
        self.event = event
        self.errors_count = errors_count
        self.wait_timeout = wait_timeout
        self.alarm_label = alarm_label
        self.info_label = info_label
        self.status_label = status_label
        self.start_button = start_button
        self.forest_button = forest_button

    def _get_default_options(self) -> uc.ChromeOptions | Options:

        if platform.system() == 'Windows':
            options = uc.ChromeOptions()
            options.binary_location = CHROME_PATH
            options.add_experimental_option(
                'excludeSwitches',
                ['enable-automation'],
            )
            options.add_argument("--disable-application-cache")
            options.add_argument("--disk-cache-size=0")
            options.add_argument("--disable-gcm")
            options.add_experimental_option(
                "excludeSwitches",
                ["enable-logging", "disable-background-networking"],
            )

        else:
            options = webdriver.ChromeOptions()
            #  только для linux
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            options.add_experimental_option(
                'excludeSwitches', ['enable-automation'])

            # options.add_argument('--disable-gpu')

            #  экспериментально
            # options.add_argument('--single-process')
            # options.add_argument('--disable-features=V8ProxyResolver')

            #  Блокируем уведомления(ломает бой)
            # options.add_argument('--disable-notifications')

            #  Разрешить старые плагины
            # options.add_argument('--allow-outdated-plugins')
            #  Автозагрузка плагинов
            # options.add_argument('--always-authorize-plugins')

        #  Общие настройки
        #  Работа в полном окне
        options.add_argument('--start-maximized')
        # Анти-детект
        options.add_argument(
            '--disable-blink-features=AutomationControlled',
        )
        #  Только DOM
        options.set_capability("pageLoadStrategy", "eager")
        options.add_experimental_option('useAutomationExtension', False)
        #  Ускоряет загрузку
        options.add_argument('--disable-plugins-discovery')
        #  Отключает расширения
        options.add_argument('--disable-extensions')

        return options

    @property
    def cycle_is_running(self) -> bool:
        """Цикл запущен."""
        return self.event.is_set()

    @staticmethod
    def get_element_content(element: WebElement) -> Optional[str]:
        """Возвращает содержимое элемента в виде строки."""
        return element.get_attribute('outerHTML')

    @staticmethod
    def get_attr_from_element(element: WebElement, attr: str) -> Optional[str]:
        """Вытаскивает регуляркой значение атрибута из элемента."""
        text = element.get_attribute('outerHTML')
        if not text:
            return None
        pattern = rf'{attr}="([^"]+)"'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None

    def start_driver(self) -> None:
        """Создаёт объект класса webdriver учитывая self.options."""
        self.close_driver()

        if self.driver is None:

            try:
                service = Service(
                    executable_path=ChromeDriverManager().install(),
                    service_args=['--verbose'],
                )

                self.driver = webdriver.Chrome(
                    service=service,
                    options=self.options,
                )

                self.driver.set_page_load_timeout(self.wait_timeout)
                self.driver.set_script_timeout(self.wait_timeout)

            except Exception as e:
                configure_logging()
                logging.exception(
                    f'\nВозникло исключение {str(e)}\n',
                    stack_info=False,
                )

    def close_driver(self) -> None:
        """Закрывает активный driver если таковой имеется."""
        if self.driver is not None:
            try:
                self.driver.quit()
            except Exception as e:
                configure_logging()
                logging.exception(
                    f'\nВозникло исключение {str(e)}\n',
                    stack_info=False,
                )
            finally:
                self.driver = None
                self.thread = None

    def get_active_driver(self) -> Optional[webdriver.Chrome]:
        """Функция для проверки наличия активного драйвера."""
        return self.driver

    def save_url_content(self) -> None:
        """Сохраняет контент страницы.

        В файле page.html в корне проекта.
        """
        if not self.driver:
            raise InvalidSessionIdException

        page_source = self.driver.page_source
        with open('page.html', 'w', encoding='utf-8') as file:
            file.write(page_source)

    def start_event(self) -> None:
        """Устанавливает флаг в положение True."""
        self.event.set()

    def stop_event(self) -> None:
        """Устанавливает флаг в положение False."""
        self.event.clear()

    def wait_while_element_will_be_clickable(
            self, element: WebElement) -> None:
        """Ждёт пока элемент станет кликабельным."""
        if self.driver:
            WebDriverWait(self.driver, 5).until(
                ec.element_to_be_clickable(element))

    def scroll_to_element(self, element: WebElement) -> None:
        """Прокручивает до нужного жлемента."""
        if self.driver:
            self.driver.execute_script(
                "arguments[0].scrollIntoView();",
                element,
            )

    def click_to_element_with_actionchains(self, element: WebElement) -> None:
        """Щёлкает по элементу методом click класса ActionChains.

        Максимальная эмуляция реального нажатия мышкой*
        """
        if self.driver:
            ActionChains(self.driver).move_to_element(
                    element).click().perform()

    def send_alarm_message(
            self,
            text: str = '') -> None:
        """Меняет текст alarm_label Tkinter."""
        self.alarm_label.configure(
            text=text,
        ) if self.alarm_label else print(text)

    def send_info_message(
            self,
            text: str = '') -> None:
        """Меняет текст info_label Tkinter."""
        self.info_label.configure(
            text=text,
        ) if self.info_label else print(text)

    def send_status_message(
            self,
            text: str = '') -> None:
        """Меняет текст status_label Tkinter."""
        self.status_label.configure(
            text=text,
        ) if self.status_label else print(text)

    def clean_label_messages(self) -> None:
        """Очищает все уведомления."""
        self.send_alarm_message()
        self.send_info_message()
        self.send_status_message()

    def is_alert_present(self) -> Optional[bool]:
        """Метод определения наличия уведомления на странице."""
        if not self.driver:
            raise InvalidSessionIdException

        try:
            self.driver.switch_to.alert
            return True
        except NoAlertPresentException:
            return False

    def sleep_while_event_is_true(
            self, time_to_sleep: int) -> None:
        """Ждёт указанное количество секунд.

        Пока флаг event == True.
        :time_to_sleep: кол-во секунд для ожидания.
        """
        counter = time_to_sleep
        while self.cycle_is_running and counter > 0:
            sleep(1)
            counter -= 1
            self.send_status_message(
                text=f'Ждём секунд: {counter}',
            )
        self.send_status_message()
