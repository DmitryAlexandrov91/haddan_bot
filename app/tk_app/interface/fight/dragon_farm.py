import threading
import tkinter as tk

from selenium.common.exceptions import InvalidSessionIdException
from tk_app.core import app
from tk_app.driver_manager import manager
from tk_app.interface.login import send_message_checkbox_value, tg_id_field

from .quick_slots import fight_slot, get_round_spells, spell_slot


#  Функции фарма драконов.
def start_dragon_farm():
    print('Начинаем фарм дракона.')
    dragon_farm_start_button.configure(foreground='green')
    manager.start_event()

    try:
        manager.dragon_farm(
            default_slot=fight_slot.get(),
            default_spell=spell_slot.get(),
            spell_book=get_round_spells(),
            message_to_tg=send_message_checkbox_value.get(),
            telegram_id=tg_id_field.get().strip()
        )

    except InvalidSessionIdException:
        pass


def stop_dragon_farm():
    manager.stop_event()
    dragon_farm_start_button.configure(foreground='black')
    print('Останавливаю фарм драконов')


def start_dragon_thread():
    manager.stop_event()
    manager.event.thread = threading.Thread(
        target=start_dragon_farm, daemon=True)
    manager.event.thread.start()


#  Кнопки запуска и остановки фарма драконов. --------------------------------
dragon_farm_label = tk.Label(
    app,
    text='Фарм драконов',
    bg='#FFF4DC')
dragon_farm_label.grid(row=3, column=5, columnspan=2)

dragon_farm_start_button = tk.Button(
    app,
    text='старт',
    width=9,
    bg='#FFF4DC',
    command=start_dragon_thread
    )
dragon_farm_start_button.grid(
    row=4, column=5
)

dragon_farm_stop_button = tk.Button(
    app,
    text='стоп',
    width=9,
    bg='#FFF4DC',
    command=stop_dragon_farm
    )
dragon_farm_stop_button.grid(
    row=4, column=6
)
#  --------------------------------------------------------------------
