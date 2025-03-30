import threading
import tkinter as tk

from bot_classes import DriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from tk_app.core import app
from tk_app.driver_manager import manager


def test(manager: DriverManager):
    manager.driver.switch_to.default_content()
    slots_2 = manager.driver.find_elements(
        By.CSS_SELECTOR,
        'a[href="javascript:qs_toggleSlots()"]'
    )
    if slots_2:
        print(slots_2)
        manager.print_element_content(slots_2[0])
        slots_2[0].click()


def test_2(manager: DriverManager):

    slots = manager.driver.find_elements(
        By.CSS_SELECTOR,
        'a[href="javascript:Slot.showSlots()"]'
    )
    if slots:
        print(slots)
        manager.print_element_content(slots[0])
        try:
            slots[0].click()
        except Exception:
            print('Слот закрыт')
            pass


def start_test_thread():
    manager.stop_event()
    manager.event.thread = threading.Thread(target=test(manager=manager))
    manager.event.thread.start()


def start_test_thread_2():
    manager.stop_event()
    manager.event.thread = threading.Thread(target=test_2(manager=manager))
    manager.event.thread.start()


test_btn = tk.Button(
    app,
    text='открыть',
    width=9,
    bg='#FFF4DC',
    command=start_test_thread
    )
test_btn.grid(
    row=7, column=5
)


test_btn_2 = tk.Button(
    app,
    text='закрыть',
    width=9,
    bg='#FFF4DC',
    command=start_test_thread_2
    )
test_btn_2.grid(
    row=7, column=6
)
