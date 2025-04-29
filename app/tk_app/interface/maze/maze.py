"""Фарм в лабиринте."""
import threading
import tkinter as tk

from bot_classes import DriverManager
from constants import Floor
from maze_utils import get_floor_map
from tk_app.core import app
from tk_app.driver_manager import manager
from tk_app.interface.fight import (cheerfulness_drink_checkbox_value,
                                    cheerfulness_drink_field,
                                    cheerfulness_slot, cheerfulness_spell,
                                    main_slots_page, main_spell_slot,
                                    min_hp_field, mind_spirit_checkbox_value,
                                    send_message_checkbox_value, tg_id_field)
from tk_app.interface.fight.quick_slots import get_round_spells

from .validators import send_message_and_stop_cycle


def start_maze_passing():
    """Точка входа в цикл farm."""
    if not manager.driver:
        manager.send_alarm_message(
            'Сначала войдите в игру!')
        exit()

    manager.start_event()
    maze_passing_start_button.configure(foreground="green")
    manager.send_alarm_message()

    mind_spirit_play = mind_spirit_checkbox_value.get()
    send_message_to_tg = send_message_checkbox_value.get()
    user_telegram_id = tg_id_field.get().strip()
    minimum_hp = min_hp_field.get().strip()
    to_the_room = direct_path_field.get().strip()
    first_floor = first_floor_checkbox_value.get()
    second_floor = second_floor_checkbox_value.get()
    third_floor = third_floor_checkbox_value.get()
    via_drop = via_drop_checkbox_value.get()

    if not first_floor and not second_floor and not third_floor:
        send_message_and_stop_cycle(
            message='Выберите этаж, на котором вы находитесь!',
            manager=manager
        )

    temp_manager = DriverManager()
    manager.send_status_message(
            text='Рисуем маршрут по наводке от Макса...',
        )

    if first_floor:
        labirint_map = get_floor_map(
            floor=Floor.FIRST_FLOOR,
            manager=temp_manager)
    if second_floor:
        labirint_map = get_floor_map(
            floor=Floor.SECOND_FLOOR,
            manager=temp_manager
            )
    if third_floor:
        labirint_map = get_floor_map(
            floor=Floor.THIRD_FLOOR,
            manager=temp_manager
            )

    if not labirint_map:
        send_message_and_stop_cycle(
            message=(
                'Не получилось нарисовать маршрут, '
                'попробуйте ещё раз.'
            ),
            manager=manager
        )

    try:

        manager.maze_passing(
                labirint_map=labirint_map,
                via_drop=via_drop,
                to_the_room=int(to_the_room) if to_the_room else None,
                slots=main_slots_page.get(),
                spell=main_spell_slot.get(),
                mind_spirit_play=mind_spirit_play,
                message_to_tg=send_message_to_tg,
                telegram_id=int(
                    user_telegram_id
                ) if user_telegram_id else None,
                min_hp=int(minimum_hp) if minimum_hp else 0,
                spell_book=get_round_spells(),
                cheerfulness=cheerfulness_drink_checkbox_value.get(),
                cheerfulness_min=int(cheerfulness_drink_field.get().strip()),
                cheerfulness_slot=cheerfulness_slot.get(),
                cheerfulness_spell=cheerfulness_spell.get(),
                first_floor=first_floor_checkbox_value.get(),
                second_floor=second_floor_checkbox_value.get(),
                third_floor=third_floor_checkbox_value.get()
            )

    except Exception as e:
        manager.send_alarm_message(
            f'При старте прохождения лабиринта возникла ошибка - {e}'
        )

    finally:
        manager.send_alarm_message()
        manager.send_status_message('Бот готов к работе')


def start_maze_passing_thread():
    if not manager.cycle_thread or not manager.cycle_thread.is_alive():
        manager.stop_event()
        manager.cycle_thread = threading.Thread(
            target=start_maze_passing, daemon=True)
        manager.cycle_thread.start()
    else:
        manager.send_alarm_message(
            'Сначала завершите активный цикл!'
        )


def stop_maze_passing():
    manager.stop_event()
    if manager.cycle_thread.is_alive():
        manager.send_status_message('Останавливаем прохождение лабиринта')
        manager.send_alarm_message('Дождитесь завершения цикла')
    else:
        manager.send_alarm_message()
        manager.send_status_message(
            'Бот готов к работе'
        ) if manager.driver else manager.send_alarm_message(
            'Игра не запущена'
        )
    maze_passing_start_button.configure(foreground='black')


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

via_drop_checkbox_value = tk.BooleanVar(value=False)


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


first_floor_checkbox_value = tk.BooleanVar(value=False)


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
