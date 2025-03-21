"""Тест асинхронного парсинга страницы http://ordenpegasa.ru/shop/"""
from time import sleep

from playwright.async_api import async_playwright
import asyncio

from constants import SHOP_URL, RES_LIST, FIELD_PRICES


async def res_price_finder(page, res):
    """Асинхронно находит цену ресурса."""
    # Ищем элемент с ресурсом и кликаем на него
    res_label = await page.query_selector(f'input[value="{res}"]')
    if res_label:
        await res_label.click()

    # Ждём появления таблицы с ценами
    await page.wait_for_selector('table[id="response"]')

    # Получаем все строки таблицы
    all_shops = await page.query_selector('table[id="response"]')
    shops = await all_shops.query_selector_all('tr')

    # Извлекаем цену из первой строки
    first_shop_price = await shops[1].inner_text()
    first_shop_price = first_shop_price.split()

    # Возвращаем цену в зависимости от формата
    if len(first_shop_price) == 4:
        return first_shop_price[2]
    return first_shop_price[3]


async def delayed_task(page, res, delay):
    """Обёртка для добавления задержки перед выполнением задачи."""
    await asyncio.sleep(delay)  # Задержка перед выполнением задачи
    return await res_price_finder(page, res)


async def get_glade_price_list():
    """Асинхронно возвращает словарь с ценами ресурсов поляны."""
    async with async_playwright() as p:
        # Запускаем браузер
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Переходим на страницу магазина
        await page.goto(SHOP_URL)

        # Кликаем на кнопку "Поляна"
        glade_button = await page.query_selector('label[for="tab_4"]')
        if glade_button:
            await glade_button.click()

        # Ждём загрузки контента
        await page.wait_for_timeout(1000)  # Задержка 1 секунда

        result_dict = {}
        for res in RES_LIST:
            price = await res_price_finder(page, res)
            result_dict[res] = float(price)
            await asyncio.sleep(2)  # Задержка 2 секунды между задачами

        # Закрываем браузер
        await browser.close()

    return result_dict

# Запуск асинхронной функции
if __name__ == '__main__':
    prices = asyncio.run(get_glade_price_list())
    print(prices)
