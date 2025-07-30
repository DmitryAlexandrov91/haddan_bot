"""Утилитки приложения haddan_bot."""
import re
import tempfile
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
