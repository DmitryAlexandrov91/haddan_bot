"""Управление фармом поляны"""
import os
import threading
import tkinter as tk
from time import sleep

from selenium.common.exceptions import InvalidSessionIdException

from tk_app.core import app
from tk_app.driver_manager import manager
from tk_app.interface.login import send_message_checkbox_value, tg_id_field
from tk_app.interface.fight import fight_slot, spell_slot, get_round_spells

from .glade_prices import GLADE_PRICES

from tk_app.interface.login import start_login_thread, stop_bot


def tk_glade_farm():
    manager.start_event()

    send_message_to_tg = send_message_checkbox_value.get()
    user_telegram_id = tg_id_field.get().strip()

    try:
        manager.glade_farm(
                price_dict=GLADE_PRICES,
                message_to_tg=send_message_to_tg,
                telegram_id=user_telegram_id,
                slots=fight_slot.get(),
                spell=spell_slot.get(),
                spell_book=get_round_spells()
            )
    except InvalidSessionIdException:
        print('Ошибка, перезапускаем драйвер.')
        stop_farm()
        stop_bot()
        start_login_thread()
        sleep(5)
        start_glade_farm_thread()


def stop_farm():
    manager.event.clear()
    glade_farm_start_buttton.configure(foreground="black")
    print('Останавливаю фарм поляны')


def start_glade_farm_thread():
    glade_farm_start_buttton.configure(foreground="green")
    manager.thread = threading.Thread(target=tk_glade_farm, daemon=True)
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
    command=start_glade_farm_thread
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
    row=11, column=1
)
