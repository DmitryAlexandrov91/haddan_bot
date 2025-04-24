# import gc
import threading
import tkinter as tk
from time import sleep

from constants import SLOT_VALUES
from selenium.common.exceptions import InvalidSessionIdException
from tk_app.core import app
from tk_app.driver_manager import manager
from tk_app.interface.login import (send_message_checkbox_value,
                                    start_login_thread, stop_bot, tg_id_field)

from .quick_slots import get_round_spells, main_slots_page, main_spell_slot


#  Функции блока автобоя. ------------------------------
def start_farm():
    print('Начинаю фарм')
    fight_start_btn.configure(foreground='green')
    manager.send_alarm_message()

    manager.start_event()
    manager.send_status_message(
        text='Фарм включен'
    )

    telegram_id = tg_id_field.get().strip()
    min_hp = min_hp_field.get().strip()

    up_down_move = up_down_checkbox_value.get()
    left_right_move = left_right_checkbox_value.get()
    mind_spirit_play = mind_spirit_checkbox_value.get()
    send_message_to_tg = send_message_checkbox_value.get()
    user_telegram_id = int(telegram_id) if telegram_id else None
    minimum_hp = int(min_hp) if min_hp else 0

    try:

        manager.farm(
            slots=main_slots_page.get(),
            spell=main_spell_slot.get(),
            up_down_move=up_down_move,
            left_right_move=left_right_move,
            mind_spirit_play=mind_spirit_play,
            message_to_tg=send_message_to_tg,
            telegram_id=user_telegram_id,
            min_hp=minimum_hp,
            spell_book=get_round_spells(),
            cheerfulness=cheerfulness_drink_checkbox_value.get(),
            cheerfulness_min=int(cheerfulness_drink_field.get().strip()),
            cheerfulness_slot=cheerfulness_slot.get(),
            cheerfulness_spell=cheerfulness_spell.get()
        )

    except InvalidSessionIdException:
        print('Драйвер не обнаружен, перезагрузка.')
        stop_farm()
        sleep(5)
        stop_bot()
        sleep(5)
        start_login_thread()
        sleep(5)
        start_thread()

    finally:
        manager.send_status_message('Бот готов к работе')
        manager.send_alarm_message()


def stop_farm():
    manager.stop_event()
    if manager.cycle_thread.is_alive():
        manager.send_status_message('Останавливаем фарм')
        manager.send_alarm_message('Дождитесь завершения цикла')
    else:
        manager.send_status_message('Бот готов к работе')
    fight_start_btn.configure(foreground='black')


def start_thread():
    if not manager.cycle_thread or not manager.cycle_thread.is_alive():
        manager.stop_event()
        manager.cycle_thread = threading.Thread(
            target=start_farm, daemon=True
        )
        manager.cycle_thread.start()
    else:
        manager.send_alarm_message(
            'Сначала завершите активный цикл!'
        )
#  --------------------------------------------------------------------


#  Титульник блока автобоя. ----------------------------------
fight_panel_label = tk.Label(
    app,
    text='Фарм',
    bg='#FFF4DC')
fight_panel_label.grid(row=0, column=5)
#  --------------------------------------------------------------------

#  Кнопки запуска и остановки боя. ------------------------------------
fight_start_btn = tk.Button(
    app,
    text='старт',
    width=9,
    bg='#FFF4DC',
    command=start_thread
    )
fight_start_btn.grid(
    row=2, column=5
)

fight_stop_btn = tk.Button(
    app,
    text='стоп',
    width=9,
    bg='#FFF4DC',
    command=stop_farm
    )
fight_stop_btn.grid(
    row=2, column=6
)
#  --------------------------------------------------------------------


#  Чек боксы  ---------------------------------------------------------
left_right_checkbox_value = tk.BooleanVar(value=False)
up_down_checkbox_value = tk.BooleanVar(value=False)
mind_spirit_checkbox_value = tk.BooleanVar(value=True)
cheerfulness_drink_checkbox_value = tk.BooleanVar(value=False)


up_down_move_check_button = tk.Checkbutton(
    app,
    text="Бегать верх-вниз",
    variable=up_down_checkbox_value,
    bg='#FFF4DC'
)
up_down_move_check_button.grid(
    row=2,
    column=4,
    sticky='w'
)

left_right_move_check_button = tk.Checkbutton(
    app,
    text="Бегать влево-вправо",
    variable=left_right_checkbox_value,
    bg='#FFF4DC'
)
left_right_move_check_button.grid(
    row=3,
    column=4,
    sticky='w'
)

mind_spiritplay_check_button = tk.Checkbutton(
    app,
    text="Автоигра с духом ума",
    variable=mind_spirit_checkbox_value,
    bg='#FFF4DC'
)
mind_spiritplay_check_button.grid(
    row=4,
    column=4,
    sticky='nw'
)

min_hp_label = tk.Label(
    app,
    text='Минимум ХП',
    bg='#FFF4DC'
)
min_hp_label.grid(
    row=5, column=4,
    sticky='w'
)
min_hp_field = tk.Entry(
    app, width=8, justify='center'
)
min_hp_field.grid(
    row=5, column=4
)

#  Блок  бодрости
cheerfulness_drink_check_button = tk.Checkbutton(
    app,
    text='Пить бодру',
    variable=cheerfulness_drink_checkbox_value,
    bg='#FFF4DC'
)
cheerfulness_drink_check_button.grid(
    row=6, column=4, sticky='w')

cheerfulness_level_label = tk.Label(
    app,
    text='Минимум бодры',
    bg='#FFF4DC'
)
cheerfulness_level_label.grid(
    row=7, column=4, sticky='w'
)

cheerfulness_drink_field = tk.Entry(
    app, width=3, justify='center'
)
cheerfulness_drink_field.grid(
    row=7, column=4
)
cheerfulness_drink_field.insert(0, 95)

cheerfulness_slot = tk.StringVar(app)
cheerfulness_slot.set(1)

cheerfulness_spell = tk.StringVar(app)
cheerfulness_spell.set(1)

cheerfulness_slot_label = tk.OptionMenu(
    app, cheerfulness_slot, *SLOT_VALUES
)
cheerfulness_slot_label.grid(row=6, column=4)

cheerfulness_spell_label = tk.OptionMenu(
    app, cheerfulness_spell, *SLOT_VALUES,
)
cheerfulness_spell_label.grid(row=6, column=4, sticky='e')
#  --------------------------------------------------------------------
