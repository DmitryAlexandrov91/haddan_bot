# Блок проведения сложного боя с отхилом и несколькими заклами
# В разработке, пока работает через задницу
import threading
import tkinter as tk

from tk_app.core import app
from tk_app.driver_manager import manager

from .fight import (left_right_checkbox_value, mind_spirit_checkbox_value,
                    up_down_checkbox_value,
                    fight_slot, spell_slot)


values = ("1", "2", "3", "4", "5", "6", "7")


def start_heavy_fight():
    print('Начинаю сложный автобой')
    manager.start_event()

    up_down_move = up_down_checkbox_value.get()
    left_right_move = left_right_checkbox_value.get()
    mind_spirit_play = mind_spirit_checkbox_value.get()
    additional_spells = additional_spells_checkbox_value.get()

    # manager.heavy_farm(
    #     main_fight_slot=fight_slot.get(),
    #     main_fight_spell=spell_slot.get(),
    #     treatment_slot=treatment_slot.get(),
    #     treatment_spell=treatment_spell.get(),
    #     fight_slot_2=skill_fight_2_slot_choice.get(),
    #     fight_spell_2=skill_fight_2_spell_choice.get(),
    #     fight_slot_3=skill_fight_3_slot_choice.get(),
    #     fight_spell_3=skill_fight_3_spell_choice.get(),
    #     fight_slot_4=skill_fight_4_slot_choice.get(),
    #     fight_spell_4=skill_fight_4_spell_choice.get(),
    #     fight_slot_5=skill_fight_5_slot_choice.get(),
    #     fight_spell_5=skill_fight_5_spell_choice.get(),
    #     up_down_move=up_down_move,
    #     left_right_move=left_right_move,
    #     mind_spirit_play=mind_spirit_play,
    #     additional_spells=additional_spells,
    # )


def stop_heavy_fight():
    manager.stop_event()
    manager.choises.clear()
    print('Останавливаю автобой')


def start_heavy_thread():
    manager.stop_event()
    manager.event.thread = threading.Thread(target=start_heavy_fight)
    manager.event.thread.start()


#  Кнопки запуска и остановки боя. ---------------------------------
heavy_fight_start_btn = tk.Button(
    app,
    text='старт',
    width=9,
    bg='#FFF4DC',
    command=start_heavy_thread
    )
heavy_fight_start_btn.grid(
    row=7, column=5
)

heavy_fight_stop_btn = tk.Button(
    app,
    text='стоп',
    width=9,
    bg='#FFF4DC',
    command=stop_heavy_fight
    )
heavy_fight_stop_btn.grid(
    row=7, column=6
)
#  ------------------------------------------------------------------

#  Титульник блока тяжелого боя. ------------------------------------
heavy_fight = tk.Label(
    app,
    text='Проведение боя с отхилом и доп ударами.',
    bg='#FFF4DC')
heavy_fight.grid(row=5, column=5)
#  ------------------------------------------------------------------

# Кнопки закла для отхила -----------------------------------------
treatment_label = tk.Label(
    app,
    text='Закл для отхила (страница, слот)',
    bg='#FFF4DC')
treatment_label.grid(row=6, column=4)

treatment_slot = tk.StringVar(app)
treatment_slot.set(values[3])

treatment_spell = tk.StringVar(app)
treatment_spell.set(values[0])

treatment_slot_label = tk.OptionMenu(
    app, treatment_slot, *values,
)
treatment_slot_label.grid(row=6, column=5)

treatment_spell_label = tk.OptionMenu(
    app, treatment_spell, *values,
)
treatment_spell_label.grid(row=6, column=6)
#  ------------------------------------------------------------------

# Боевой закл 2 -----------------------------------------------------
skill_fight_label_2 = tk.Label(
    app,
    text='Боевой закл 2(страница, слот)',
    bg='#FFF4DC')
skill_fight_label_2.grid(row=8, column=4)

skill_fight_2_slot_choice = tk.StringVar(app)
skill_fight_2_slot_choice.set(values[1])

skill_fight_2_spell_choice = tk.StringVar(app)
skill_fight_2_spell_choice.set(values[1])

skill_fight_2_label = tk.OptionMenu(
    app, skill_fight_2_slot_choice, *values,
)
skill_fight_2_label.grid(row=8, column=5)

skill_fight_2_spell_label = tk.OptionMenu(
    app, skill_fight_2_spell_choice, *values,
)
skill_fight_2_spell_label.grid(row=8, column=6)
#  ------------------------------------------------------------------

# Боевой закл 3 -----------------------------------------------------
skill_fight_label_3 = tk.Label(
    app,
    text='Боевой закл 3(страница, слот)',
    bg='#FFF4DC')
skill_fight_label_3.grid(row=9, column=4)

skill_fight_3_slot_choice = tk.StringVar(app)
skill_fight_3_slot_choice.set(values[1])

skill_fight_3_spell_choice = tk.StringVar(app)
skill_fight_3_spell_choice.set(values[2])

skill_fight_3_label = tk.OptionMenu(
    app, skill_fight_3_slot_choice, *values,
)
skill_fight_3_label.grid(row=9, column=5)

skill_fight_3_spell_label = tk.OptionMenu(
    app, skill_fight_3_spell_choice, *values,
)
skill_fight_3_spell_label.grid(row=9, column=6)
#  ------------------------------------------------------------------

# Боевой закл 4 -----------------------------------------------------
skill_fight_label_4 = tk.Label(
    app,
    text='Боевой закл 4(страница, слот)',
    bg='#FFF4DC')
skill_fight_label_4.grid(row=10, column=4)

skill_fight_4_slot_choice = tk.StringVar(app)
skill_fight_4_slot_choice.set(values[1])

skill_fight_4_spell_choice = tk.StringVar(app)
skill_fight_4_spell_choice.set(values[3])

skill_fight_4_label = tk.OptionMenu(
    app, skill_fight_4_slot_choice, *values,
)
skill_fight_4_label.grid(row=10, column=5)

skill_fight_4_spell_label = tk.OptionMenu(
    app, skill_fight_4_spell_choice, *values,
)
skill_fight_4_spell_label.grid(row=10, column=6)
#  ------------------------------------------------------------------

# Боевой закл 5 -----------------------------------------------------
skill_fight_label_5 = tk.Label(
    app,
    text='Боевой закл 5(страница, слот)',
    bg='#FFF4DC')
skill_fight_label_5.grid(row=11, column=4)

skill_fight_5_slot_choice = tk.StringVar(app)
skill_fight_5_slot_choice.set(values[1])

skill_fight_5_spell_choice = tk.StringVar(app)
skill_fight_5_spell_choice.set(values[5])

skill_fight_5_label = tk.OptionMenu(
    app, skill_fight_5_slot_choice, *values,
)
skill_fight_5_label.grid(row=11, column=5)

skill_fight_5_spell_label = tk.OptionMenu(
    app, skill_fight_5_spell_choice, *values,
)
skill_fight_5_spell_label.grid(row=11, column=6)
#  ------------------------------------------------------------------

additional_spells_checkbox_value = tk.IntVar(value=0)

additional_spells_check_button = tk.Checkbutton(
    app,
    text="Использовать доп. удары",
    variable=additional_spells_checkbox_value,
    bg='#FFF4DC'
)
additional_spells_check_button.grid(
    row=7,
    column=4
)
