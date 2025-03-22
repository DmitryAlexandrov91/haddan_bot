import tkinter as tk
import threading

from tk_app.core import app

from tk_app.driver_manager import manager

from constants import FIELD_PRICES

GLADE_PRICES = FIELD_PRICES.copy()


def tk_glade_farm():

    manager.glade_farm(
            price_dict=GLADE_PRICES)
    print('Начинаю фарм поляны')


def stop_farm():
    manager.stop_farm()
    print('Останавливаю фарм поляны')


def start_thread():
    manager.thread = threading.Thread(target=tk_glade_farm)
    manager.thread.start()


glade__farm_lable = tk.Label(
    app,
    text='Фарм поляны.',
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
