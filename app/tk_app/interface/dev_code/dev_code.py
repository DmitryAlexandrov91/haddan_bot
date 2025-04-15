import threading
import tkinter as tk
from time import sleep  # noqa

from bot_classes import DriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from tk_app.core import app
from tk_app.driver_manager import manager


def test_1(manager: DriverManager):
    # element = manager.driver.find_elements(By.ID, 'slotsBtn4')
    # if element:
    #     manager.print_element_content(element=element[0])
    try:
        manager.driver.execute_script("slotsShow(3)")
        sleep(1)
        manager.driver.execute_script(
            'return qs_onClickSlot(event, 0)'
        )
    except Exception:
        print('Не удалось выполнить действие с элементом')

    # else:
    #     print('Элемент не найден!')


def test_2(manager: DriverManager):
    pass


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
    command=start_test_thread
    )
test_btn.grid(
    row=7, column=5
)


test_btn_2 = tk.Button(
    app,
    text='тест 2',
    width=9,
    bg='#FFF4DC',
    command=start_test_thread_2
    )
test_btn_2.grid(
    row=7, column=6
)
