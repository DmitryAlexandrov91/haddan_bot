"""Фарм в лабиринте."""
import threading
import tkinter as tk
from time import sleep

from tk_app.core import app
from tk_app.driver_manager import manager
from tk_app.interface.fight import (cheerfulness_drink_checkbox_value,
                                    cheerfulness_drink_field,
                                    cheerfulness_slot, cheerfulness_spell,
                                    main_slots_page, main_spell_slot,
                                    min_hp_field, mind_spirit_checkbox_value,
                                    send_message_checkbox_value, tg_id_field)
from tk_app.interface.fight.quick_slots import get_round_spells


def maze_passing():
    print('Начинаем прохождение лаба')
    manager.start_event()

    mind_spirit_play = mind_spirit_checkbox_value.get()
    send_message_to_tg = send_message_checkbox_value.get()
    user_telegram_id = int(tg_id_field.get().strip())
    minimum_hp = int(min_hp_field.get().strip())

    manager.maze_passing(
            via_drop=via_drop_checkbox_value.get(),
            to_the_room=int(direct_path_field.get().strip()),
            slots=main_slots_page.get(),
            spell=main_spell_slot.get(),
            mind_spirit_play=mind_spirit_play,
            message_to_tg=send_message_to_tg,
            telegram_id=user_telegram_id,
            min_hp=minimum_hp,
            spell_book=get_round_spells(),
            cheerfulness=cheerfulness_drink_checkbox_value.get(),
            cheerfulness_min=int(cheerfulness_drink_field.get().strip()),
            cheerfulness_slot=cheerfulness_slot.get(),
            cheerfulness_spell=cheerfulness_spell.get(),
        )


def start_maze_passing_thread():
    manager.stop_event()
    maze_passing_start_button.configure(foreground="green")
    manager.event.thread = threading.Thread(target=maze_passing, daemon=True)
    manager.event.thread.start()


def stop_maze_passing():
    manager.stop_event()
    while manager.event.thread.is_alive():
        sleep(1)
    maze_passing_start_button.configure(foreground='black')
    print('Останавливаем прохождение лаба')


maze_farm_label = tk.Label(
    app,
    text='Прохождение лабиринта ->',
    bg='#FFF4DC'
)
maze_farm_label.grid(row=11, column=0)

maze_passing_start_button = tk.Button(
    app,
    text='старт',
    width=9,
    bg='#FFF4DC',
    command=start_maze_passing_thread
    )
maze_passing_start_button.grid(
    row=11, column=1
)

maze_passing_stop_button = tk.Button(
    app,
    text='стоп',
    width=9,
    bg='#FFF4DC',
    command=stop_maze_passing
    )
maze_passing_stop_button.grid(
    row=11, column=2
)

direct_path_label = tk.Label(
    app,
    text='До комнаты №',
    bg='#FFF4DC'
)
direct_path_label.grid(row=12, column=0, sticky='w')

direct_path_field = tk.Entry(
    app, width=4
)
direct_path_field.grid(row=12, column=0, sticky='e')

via_drop_checkbox_value = tk.BooleanVar(value=True)


via_drop_checkbox_button = tk.Checkbutton(
    app,
    text="Через весь дроп",
    variable=via_drop_checkbox_value,
    bg='#FFF4DC'
)
via_drop_checkbox_button.grid(
    row=12,
    column=1,
)


first_floor_checkbox_value = tk.BooleanVar(value=True)


first_floor_checkbox_button = tk.Checkbutton(
    app,
    text="Этаж 1",
    variable=first_floor_checkbox_value,
    bg='#FFF4DC'
)
first_floor_checkbox_button.grid(
    row=13,
    column=0,
)


second_floor_checkbox_value = tk.BooleanVar(value=False)


second_floor_checkbox_button = tk.Checkbutton(
    app,
    text="Этаж 2",
    variable=second_floor_checkbox_value,
    bg='#FFF4DC'
)
second_floor_checkbox_button.grid(
    row=13,
    column=1,
)


third_floor_checkbox_value = tk.BooleanVar(value=False)


third_floor_checkbox_button = tk.Checkbutton(
    app,
    text="Этаж 3",
    variable=third_floor_checkbox_value,
    bg='#FFF4DC'
)
third_floor_checkbox_button.grid(
    row=13,
    column=2,
)
