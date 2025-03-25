import tkinter as tk
import threading

from tk_app.core import app
from tk_app.driver_manager import manager


def start_fight():
    print('Начинаю автобой')
    manager.start_event()

    manager.one_spell_fight(
        slots=fight_slot.get(),
        spell=spell_slot.get()
    )


def stop_fight():
    manager.stop_event()
    print('Останавливаю автобой')


def start_thread():
    manager.stop_event()
    manager.event.thread = threading.Thread(target=start_fight)
    manager.event.thread.start()


values = ["1", "2", "3", "4", "5", "6", "7"]

fight_slot = tk.StringVar(app)
fight_slot.set(values[1])

spell_slot = tk.StringVar(app)
spell_slot.set(values[0])

fight_panel_label = tk.Label(
    app,
    text='Проведение боя одним заклом',
    bg='#FFF4DC')
fight_panel_label.grid(row=0, column=5)

skill_fight_label = tk.Label(
    app,
    text='Закл (слот, закл)',
    bg='#FFF4DC')
skill_fight_label.grid(row=1, column=4)

slot_label = tk.OptionMenu(
    app, fight_slot, *values,
)
slot_label.grid(row=1, column=5)

spell_label = tk.OptionMenu(
    app, spell_slot, *values,
)
spell_label.grid(row=1, column=6)


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
    command=stop_fight
    )
fight_stop_btn.grid(
    row=2, column=6
)
