"""Утилитки приложения haddan_bot."""
import re
import tempfile
from datetime import datetime
from time import sleep
from typing import Any

from bot_classes import DriverManager
from constants import FIELD_PRICES, RES_LIST, SHOP_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def price_counter(resurses: list, price_diсt: dict = FIELD_PRICES) -> int:
    """Находит самый дорогой ресурс из списка и возвращает его индекс."""
    result = []
    for s in resurses:
        pattern = r'(\D+)\s+-\s+(\d+)'
        match = re.match(pattern, s)
        if match:
            part1 = match.group(1).strip()
            part2 = int(match.group(2))
            result.append(part2 * price_diсt[f'{part1}'])
    return result.index(max(result))


def time_extractor(text: str) -> int:
    """Извлекает время из строки с текстом."""
    pattern = r'-?\d+:\d+'
    matches = re.findall(pattern, text)
    if not matches:
        return 0
    time_str = matches[0]
    minutes, secundes = map(int, time_str.split(':'))
    if minutes >= 0 and secundes >= 0:
        return minutes * 60 + secundes
    return 0


def res_price_finder(driver: WebDriver, res: str) -> Any:
    """Находит цену ресурса по его названию."""
    res_label = driver.find_elements(
        By.CSS_SELECTOR,
        f'input[value="{res}"]',
    )
    if res_label:
        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable(res_label[0]))
        res_label[0].click()
    sleep(2)
    all_shops = driver.find_element(
        By.CSS_SELECTOR, 'table[id="response"]',
    )
    shops = all_shops.find_elements(
        By.TAG_NAME, 'tr',
    )
    first_shop_price = shops[1].text.split()
    if len(first_shop_price) == 4:
        return first_shop_price[2]
    return first_shop_price[3]


def get_glade_price_list(manager: DriverManager) -> dict[Any, Any]:
    """Возвращает словарь с ценами ресурсов поляны.

    Парсит поисковик по базару на сайте
    'http://ordenpegasa.ru/shop/'
    На полный цикл функции уходит примерно 15 секунд.
    """
    manager.options.add_argument('--headless')
    temp_directory = tempfile.mkdtemp()
    manager.options.add_argument(f'--user-data-dir={temp_directory}')
    manager.start_driver()
    manager.driver.get(SHOP_URL)
    glade_button = manager.driver.find_elements(
        By.CSS_SELECTOR,
        'label[for="tab_4"]',
    )
    if glade_button:
        glade_button[0].click()
    sleep(1)
    result = []
    for res in RES_LIST:
        result.append(
            res_price_finder(manager.driver, res),
        )

    result_dict = {}
    for key, value in zip(FIELD_PRICES.keys(), result):
        result_dict[key] = float(value)
    return result_dict


def get_intimidation_and_next_room(text: str) -> tuple[int, int]:
    """Вытаскивает данные из ответа духа азарта.

    1. intimidation - показатель запугивания
    2. next_room - номер следующей комнаты.
    """
    intimidation_pattern = r'Запугивание\s*-\s*(\d+)'
    match = re.search(intimidation_pattern, text)
    if match:
        intimidation = int(match.group(1))
    else:
        intimidation = 0
        print('Не удалось найти значение параметра Запугивание.')

    room_number_pattern = r'комнату №(\d+)'
    match = re.search(room_number_pattern, text)
    if match:
        next_room = int(match.group(1))
    else:
        next_room = 0
        print('Не удалось найти номер следующей комнаты.')
    return intimidation, next_room


def get_attr_from_string(text: str, attr: str) -> str | None:
    """Вытаскивает регуляркой значение атрибута из текста."""
    pattern = rf'{attr}="([^"]+)"'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


def get_dragon_time_wait(text: str) -> int:
    """Извлекает время и дату из текста вида "09:16:12 17-04-2025".

    сравнивает с текущим временем и возвращает разницу в секундах.
    """
    pattern = r"\d{2}:\d{2}:\d{2}\s\d{2}-\d{2}-\d{4}$"
    match = re.search(pattern, text)
    if match:
        wait_time_str = match.group()
    else:
        raise ValueError('Время не найдено')

    current_time = datetime.now()

    wait_time = datetime.strptime(wait_time_str, "%H:%M:%S %d-%m-%Y")

    delta = wait_time - current_time

    return int(delta.total_seconds())
