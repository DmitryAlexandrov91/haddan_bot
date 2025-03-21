"""Утилитки приложения haddan_miner"""
import os
import re
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import FIELD_PRICES, SHOP_URL, RES_LIST


def price_counter(resurses, price_diсt=FIELD_PRICES):
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


def time_extractor(text):
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


def res_price_finder(driver, res):
    res_label = driver.find_elements(
        By.CSS_SELECTOR,
        f'input[value="{res}"]'
    )
    if res_label:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(res_label[0]))
        res_label[0].click()
    sleep(2)
    all_shops = driver.find_element(
        By.CSS_SELECTOR, 'table[id="response"]'
    )
    shops = all_shops.find_elements(
        By.TAG_NAME, 'tr'
    )
    first_shop_price = shops[1].text.split()
    if len(first_shop_price) == 4:
        return first_shop_price[2]
    return first_shop_price[3]


def get_glade_price_list(manager):
    """Возвращает словарь с ценами ресурсов поляны.

    Парсит поисковик по базару на сайте
    'http://ordenpegasa.ru/shop/'
    На полный цикл функции уходит примерно 15 секунд.
    """
    manager.options.add_argument('--headless')
    manager.start_driver()
    manager.driver.get(SHOP_URL)
    glade_button = manager.driver.find_elements(
        By.CSS_SELECTOR,
        'label[for="tab_4"]'
    )
    if glade_button:
        glade_button[0].click()
    sleep(1)
    result = []
    for res in RES_LIST:
        result.append(
            res_price_finder(manager.driver, res)
        )
    result_dict = {}
    for key, value in zip(FIELD_PRICES.keys(), result):
        result_dict[key] = float(value)
    return result_dict
