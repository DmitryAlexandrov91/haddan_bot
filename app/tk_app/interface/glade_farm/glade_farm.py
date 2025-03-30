"""Управление фармом поляны"""
import os
import threading
import tkinter as tk

from tk_app.core import app
from tk_app.driver_manager import manager

from tk_app.interface.fight import send_message_checkbox_value

from .glade_prices import GLADE_PRICES


def tk_glade_farm():
    send_message_to_tg = send_message_checkbox_value.get()

    print(send_message_to_tg)

    manager.glade_farm(
            price_dict=GLADE_PRICES,
            message_to_tg=send_message_to_tg)
    print('Начинаю фарм поляны')


def stop_farm():
    manager.event.clear()
    print('Останавливаю фарм поляны')


def start_thread():
    manager.event.clear()
    manager.thread = threading.Thread(target=tk_glade_farm)
    manager.thread.start()


glade__farm_lable = tk.Label(
    app,
    text='Фарм поляны - >',
    bg='#FFF4DC')
glade__farm_lable.grid(row=2, column=0)


glade_farm_start_buttton = tk.Button(
    app,
    text='старт',
    width=9,
    bg='#FFF4DC',
    command=start_thread
    )
glade_farm_start_buttton.grid(
    row=2, column=1
)

glade_farm_stop_buttton = tk.Button(
    app,
    text='стоп',
    width=9,
    bg='#FFF4DC',
    command=stop_farm
    )
glade_farm_stop_buttton.grid(
    row=2, column=2
)

# Информационный блок


def glade_farm_txt_open():
    os.startfile('glade_farm.txt')


statistic_button = tk.Button(
    app,
    text='лог подбора трав',
    width=15,
    bg='#FFF4DC',
    command=glade_farm_txt_open
)
statistic_button.grid(
    row=12, column=1
)
