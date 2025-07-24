import threading
import tkinter as tk
from time import sleep  # noqa

from bot_classes import DriverManager
from selenium.webdriver.common.by import By

from tk_app.core import app
from tk_app.driver_manager import manager


def test_1(manager: DriverManager):
    manager.try_to_switch_to_central_frame()
    rounds = manager.driver.find_elements(
        By.ID, 'divlog')
    if rounds:
        for round in rounds:
            manager.print_element_content(round)

    else:
        print('раунды не обнаружены!!')


def test_2(manager: DriverManager):
    manager.try_to_switch_to_central_frame()
    rounds = manager.driver.find_elements(
        By.CSS_SELECTOR, '#divlog p')
    if rounds:
        if len(rounds) == 1:
            print('Раунд 2')
        else:
            amount = len(rounds)
            print(f'Раунд {amount + 1}')
    else:
        print('Раунд 1')


def start_test_thread():
    manager.stop_event()
    manager.event.thread = threading.Thread(target=test_1(manager=manager))
    manager.event.thread.start()


def start_test_thread_2():
    manager.stop_event()
    manager.event.thread = threading.Thread(target=test_2(manager=manager))
    manager.event.thread.start()


test_btn = tk.Button(
    app,
    text='тест 1',
    width=9,
    bg='#FFF4DC',
    command=start_test_thread,
    )
test_btn.grid(
    row=7, column=5,
)


test_btn_2 = tk.Button(
    app,
    text='тест 2',
    width=9,
    bg='#FFF4DC',
    command=start_test_thread_2,
    )
test_btn_2.grid(
    row=7, column=6,
)
