import threading
import tkinter as tk

from tk_app.core import app
from tk_app.driver_manager import manager


#  Функции блока боя одним заклинанием. ------------------------------
def start_fight():
    print('Начинаю автобой')
    manager.start_event()

    up_down_move = up_down_checkbox_value.get()
    left_right_move = left_right_checkbox_value.get()
    mind_spirit_play = mind_spirit_checkbox_value.get()

    manager.one_spell_farm(
        slots=fight_slot.get(),
        spell=spell_slot.get(),
        up_down_move=up_down_move,
        left_right_move=left_right_move,
        mind_spirit_play=mind_spirit_play
    )


def stop_fight():
    manager.stop_event()
    manager.choises.clear()
    print('Останавливаю автобой')


def start_thread():
    manager.stop_event()
    manager.event.thread = threading.Thread(target=start_fight)
    manager.event.thread.start()
#  --------------------------------------------------------------------


values = ("1", "2", "3", "4", "5", "6", "7")

#  Титульник блока боя одним заклом. ----------------------------------
fight_panel_label = tk.Label(
    app,
    text='Автобой',
    bg='#FFF4DC')
fight_panel_label.grid(row=0, column=5)
#  --------------------------------------------------------------------

#  Кнопки основного заклинания ----------------------------------------
skill_fight_label = tk.Label(
    app,
    text='Боевой закл (страница, слот)',
    bg='#FFF4DC')
skill_fight_label.grid(row=1, column=4)

fight_slot = tk.StringVar(app)
fight_slot.set(values[1])

spell_slot = tk.StringVar(app)
spell_slot.set(values[0])

main_slot_label = tk.OptionMenu(
    app, fight_slot, *values,
)
main_slot_label.grid(row=1, column=5)

main_spell_label = tk.OptionMenu(
    app, spell_slot, *values,
)
main_spell_label.grid(row=1, column=6)
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
    command=stop_fight
    )
fight_stop_btn.grid(
    row=2, column=6
)
#  --------------------------------------------------------------------

#  Чек боксы  ---------------------------------------------------------
left_right_checkbox_value = tk.IntVar(value=0)
up_down_checkbox_value = tk.IntVar(value=0)
mind_spirit_checkbox_value = tk.IntVar(value=True)

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
    ipadx=1,
    sticky='nw'
)
#  --------------------------------------------------------------------
