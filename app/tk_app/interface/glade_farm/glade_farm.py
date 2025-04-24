"""Управление фармом поляны"""
import threading
import tkinter as tk
from time import sleep

from constants import LABIRINT_MAP_URL
from selenium.common.exceptions import InvalidSessionIdException
from tk_app.core import app
from tk_app.driver_manager import manager
from tk_app.interface.fight import (get_round_spells, main_slots_page,
                                    main_spell_slot)
from tk_app.interface.login import (send_message_checkbox_value,
                                    start_login_thread, stop_bot, tg_id_field)

from .glade_prices import GLADE_PRICES


def tk_glade_farm():
    manager.start_event()

    send_message_to_tg = send_message_checkbox_value.get()
    user_telegram_id = tg_id_field.get().strip()

    try:
        manager.send_status_message('Начинаем фарм полянки')
        manager.glade_farm(
                price_dict=GLADE_PRICES,
                message_to_tg=send_message_to_tg,
                telegram_id=int(
                    user_telegram_id
                ) if user_telegram_id else None,
                slots=main_slots_page.get(),
                spell=main_spell_slot.get(),
                spell_book=get_round_spells()
            )
    except InvalidSessionIdException:
        print('Драйвер не обнаружен, перезагрузка.')
        stop_farm()
        sleep(5)
        stop_bot()
        sleep(5)
        start_login_thread()
        sleep(5)
        start_glade_farm_thread()

    finally:
        manager.send_status_message('Бот готов к работе')
        manager.send_alarm_message()


def stop_farm():
    manager.stop_event()
    if manager.cycle_thread.is_alive():
        manager.send_status_message('Останавливаем фарм поляны')
        manager.send_alarm_message('Дождитесь завершения цикла')
    else:
        manager.send_status_message('Бот готов к работе')
    glade_farm_start_buttton.configure(foreground="black")


def start_glade_farm_thread():
    manager.stop_event()
    glade_farm_start_buttton.configure(foreground="green")
    manager.cycle_thread = threading.Thread(target=tk_glade_farm, daemon=True)
    manager.cycle_thread.start()


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


# def glade_farm_txt_open():
#     os.startfile('glade_farm.txt')


# statistic_button = tk.Button(
#     app,
#     text='лог подбора трав',
#     width=15,
#     bg='#FFF4DC',
#     command=glade_farm_txt_open
# )
# statistic_button.grid(
#     row=11, column=1
# )


# Карта лабиринта
def open_map():
    manager.driver.execute_script("window.open('');")
    windows = manager.driver.window_handles
    manager.driver.switch_to.window(windows[-1])
    manager.driver.get(LABIRINT_MAP_URL)
    manager.driver.switch_to.window(windows[0])


labirint_map = tk.Button(
    app,
    text='карта лабиринта',
    width=15,
    bg='#FFF4DC',
    command=open_map
)
labirint_map.grid(
    row=10,
    column=1,
)
#  --------------------------------------------------------------------
