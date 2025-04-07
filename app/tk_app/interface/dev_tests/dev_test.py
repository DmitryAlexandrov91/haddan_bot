import threading
import tkinter as tk

from bot_classes import DriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from tk_app.core import app
from tk_app.driver_manager import manager

from time import sleep


def test_1():
    frames = manager.driver.find_elements(By.TAG_NAME, 'iframe')
    if frames:
        sleep(0.5)
        manager.driver.switch_to.frame("frmcenterandchat")


def test_2(manager: DriverManager):
    manager.driver.delete_cookie()


def start_test_thread():
    manager.stop_event()
    manager.event.thread = threading.Thread(target=test_1())
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
    command=test_1
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
