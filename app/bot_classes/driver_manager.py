import logging
import platform
import threading
import tkinter as tk
import re
from typing import Optional

from configs import configure_logging
from constants import CHROME_PATH
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telebot import TeleBot
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    """Класс создания и управления объектом webdriver.Chrome.

    :bot: объект класса Telebot библиотеки telebot, опционально.
    """

    def __init__(self, bot=None):
        self.driver: webdriver.Chrome = None
        self.cycle_thread: threading = None
        self.options = self._get_default_options()
        self.bot: TeleBot = bot
        self.event: threading.Event = threading.Event()
        self.errors_count: int = 0
        self.wait_timeout: int = 30
        self.alarm_label: tk.Label = None
        self.info_label: tk.Label = None
        self.status_label: tk.Label = None
        self.start_button: tk.Button = None

    def _get_default_options(self):
        options = webdriver.ChromeOptions()

        #  Работа в полном окне
        options.add_argument('--start-maximized')

        # Анти-детект
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        # options.add_argument('--disable-gpu')

        #  экспериментально
        # options.add_argument('--single-process')
        # options.add_argument('--disable-features=V8ProxyResolver')

        #  Только DOM
        options.set_capability("pageLoadStrategy", "eager")

        #  Отключает расширения
        options.add_argument('--disable-extensions')
        #  Ускоряет загрузку
        options.add_argument('--disable-plugins-discovery')
        #  Блокируем уведомления(ломает бой)
        # options.add_argument('--disable-notifications')

        #  Разрешить старые плагины
        # options.add_argument('--allow-outdated-plugins')
        #  Автозагрузка плагинов
        # options.add_argument('--always-authorize-plugins')

        if platform.system() == 'Windows':
            options.binary_location = CHROME_PATH
        else:
            #  только для linux
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

        return options

    @property
    def cycle_is_running(self):
        """Цикл запущен."""
        return self.event.is_set()

    @staticmethod
    def get_element_content(element: WebElement) -> str:
        """Возвращает содержимое элемента в виде строки."""
        return element.get_attribute('outerHTML')

    @staticmethod
    def get_attr_from_element(element: WebElement, attr: str) -> Optional[str]:
        """Вытаскивает регуляркой значение атрибута из элемента."""

        text = element.get_attribute('outerHTML')
        pattern = rf'{attr}="([^"]+)"'
        match = re.search(pattern, text)
        if match:
            title_text = match.group(1)
            return title_text

    def start_driver(self):
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
                    options=self.options
                )
                self.driver.set_page_load_timeout(self.wait_timeout)
                self.driver.set_script_timeout(self.wait_timeout)

            except Exception as e:
                configure_logging()
                logging.exception(
                    f'\nВозникло исключение {str(e)}\n',
                    stack_info=False
                )

    def close_driver(self):
        """Закрывает активный driver если таковой имеется."""
        if self.driver is not None:
            try:
                self.driver.quit()
            except Exception as e:
                configure_logging()
                logging.exception(
                    f'\nВозникло исключение {str(e)}\n',
                    stack_info=False
                )
            finally:
                self.driver = None
                self.thread = None

    def get_active_driver(self) -> webdriver.Chrome:
        """Функция для проверки наличия активного драйвера."""
        return self.driver

    def save_url_content(self):
        """Сохраняет контент страницы.

        В файле page.html в корне проекта.
        """
        page_source = self.driver.page_source
        with open('page.html', 'w', encoding='utf-8') as file:
            file.write(page_source)

    def start_event(self):
        """Устанавливает флаг в положение True."""
        self.event.set()

    def stop_event(self):
        """Устанавливает флаг в положение False."""
        self.event.clear()

    def wait_while_element_will_be_clickable(self, element: WebElement):
        """Ждёт пока элемент станет кликабельным."""
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(element))

    def scroll_to_element(self, element: WebElement):
        """Прокручивает до нужного жлемента."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            element
        )

    def click_to_element_with_actionchains(self, element: WebElement):
        """Щёлкает по элементу методом click класса ActionChains.

        Максимальная эмуляция реального нажатия мышкой*
        """
        ActionChains(self.driver).move_to_element(
                element).click().perform()

    def send_alarm_message(
            self,
            text: str = ''):
        """Меняет текст alarm_label Tkinter."""
        self.alarm_label.configure(
            text=text
        ) if self.alarm_label else print(text)

    def send_info_message(
            self,
            text: str = ''):
        """Меняет текст info_label Tkinter."""
        self.info_label.configure(
            text=text
        ) if self.info_label else print(text)

    def send_status_message(
            self,
            text: str = ''):
        """Меняет текст status_label Tkinter."""
        self.status_label.configure(
            text=text
        ) if self.status_label else print(text)

    def clean_label_messages(self):
        """Очищает все уведомления."""
        self.send_alarm_message()
        self.send_info_message()
        self.send_status_message()
