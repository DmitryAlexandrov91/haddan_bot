import tkinter as tk

from constants import SLOT_VALUES
from tk_app.core import app


def open_slots():
    current_size = (app.winfo_width(), app.winfo_height())

    max_size = 1053, 332

    if current_size == max_size:
        app.maxsize(current_size[0] - 280, current_size[1])
    else:
        app.maxsize(max_size[0], max_size[1])


quick_slots_open_btn = tk.Button(
    app,
    text='удары ->',
    width=9,
    bg='#FFF4DC',
    command=open_slots
)
quick_slots_open_btn.grid(
    row=0, column=6, sticky='w'
)

#  Кнопки основного заклинания ----------------------------------------
fight_slot = tk.StringVar(app)
fight_slot.set(SLOT_VALUES[1])

spell_slot = tk.StringVar(app)
spell_slot.set(SLOT_VALUES[0])

main_slot_label = tk.OptionMenu(
    app, fight_slot, *SLOT_VALUES
)
main_slot_label.grid(row=1, column=5)

main_spell_label = tk.OptionMenu(
    app, spell_slot, *SLOT_VALUES,
)
main_spell_label.grid(row=1, column=6)
#  --------------------------------------------------------------------


# Раунд 1 (4 удара) ----------------------------
for element in range(4):
    widget = tk.Label(
        app,
        text=f'Р1 У{element + 1}',
        bg='#FFF4DC'
    )
    widget.grid(row=0 + element, column=7)

#  Р1 У1
r1y1_slot = tk.StringVar(app)
r1y1_slot.set(SLOT_VALUES[1])
# r1y1_slot.set(fight_slot.get())

r1y1_spell = tk.StringVar(app)
r1y1_spell.set(SLOT_VALUES[0])
# r1y1_spell.set(spell_slot.get())

r1y1_slot_choise = tk.OptionMenu(
    app, r1y1_slot, *SLOT_VALUES,
)
r1y1_slot_choise.grid(row=0, column=8)

r1y1_spell_choise = tk.OptionMenu(
    app, r1y1_spell, *SLOT_VALUES,
)
r1y1_spell_choise.grid(row=0, column=9)

#  Р1 У2
r1y2_slot = tk.StringVar(app)
r1y2_slot.set(SLOT_VALUES[1])

r1y2_spell = tk.StringVar(app)
r1y2_spell.set(SLOT_VALUES[0])

r1y2_slot_choise = tk.OptionMenu(
    app, r1y2_slot, *SLOT_VALUES,
)
r1y2_slot_choise.grid(row=1, column=8)

r1y2_spell_choise = tk.OptionMenu(
    app, r1y2_spell, *SLOT_VALUES,
)
r1y2_spell_choise.grid(row=1, column=9)

#  Р1 У3
r1y3_slot = tk.StringVar(app)
r1y3_slot.set(SLOT_VALUES[1])

r1y3_spell = tk.StringVar(app)
r1y3_spell.set(SLOT_VALUES[0])

r1y3_slot_choise = tk.OptionMenu(
    app, r1y3_slot, *SLOT_VALUES,
)
r1y3_slot_choise.grid(row=2, column=8)

r1y3_spell_choise = tk.OptionMenu(
    app, r1y3_spell, *SLOT_VALUES,
)
r1y3_spell_choise.grid(row=2, column=9)


#  Р1 У4
r1y4_slot = tk.StringVar(app)
r1y4_slot.set(SLOT_VALUES[1])

r1y4_spell = tk.StringVar(app)
r1y4_spell.set(SLOT_VALUES[0])

r1y4_slot_choise = tk.OptionMenu(
    app, r1y4_slot, *SLOT_VALUES,
)
r1y4_slot_choise.grid(row=3, column=8)

r1y4_spell_choise = tk.OptionMenu(
    app, r1y4_spell, *SLOT_VALUES,
)
r1y4_spell_choise.grid(row=3, column=9)


#  Раунд 2 (4 удара) --------------------------------
for element in range(4):
    widget = tk.Label(
        app,
        text=f'Р 2 У {element + 1}',
        bg='#FFF4DC'
    )
    widget.grid(row=0 + element, column=10)

#  Р2 У1

r2y1_slot = tk.StringVar(app)
r2y1_slot.set(SLOT_VALUES[1])

r2y1_spell = tk.StringVar(app)
r2y1_spell.set(SLOT_VALUES[0])

r2y1_slot_choise = tk.OptionMenu(
    app, r2y1_slot, *SLOT_VALUES,
)
r2y1_slot_choise.grid(row=0, column=11)

r2y1_spell_choise = tk.OptionMenu(
    app, r2y1_spell, *SLOT_VALUES,
)
r2y1_spell_choise.grid(row=0, column=12)

#  Р2 У2
r2y2_slot = tk.StringVar(app)
r2y2_slot.set(SLOT_VALUES[1])

r2y2_spell = tk.StringVar(app)
r2y2_spell.set(SLOT_VALUES[0])

r2y2_slot_choise = tk.OptionMenu(
    app, r2y2_slot, *SLOT_VALUES,
)
r2y2_slot_choise.grid(row=1, column=11)

r2y2_spell_choise = tk.OptionMenu(
    app, r2y2_spell, *SLOT_VALUES,
)
r2y2_spell_choise.grid(row=1, column=12)

# #  Р2 У3
r2y3_slot = tk.StringVar(app)
r2y3_slot.set(SLOT_VALUES[1])

r2y3_spell = tk.StringVar(app)
r2y3_spell.set(SLOT_VALUES[0])

r2y3_slot_choise = tk.OptionMenu(
    app, r2y3_slot, *SLOT_VALUES,
)
r2y3_slot_choise.grid(row=2, column=11)

r2y3_spell_choise = tk.OptionMenu(
    app, r2y3_spell, *SLOT_VALUES,
)
r2y3_spell_choise.grid(row=2, column=12)

# #  Р2 У4

r2y4_slot = tk.StringVar(app)
r2y4_slot.set(SLOT_VALUES[1])

r2y4_spell = tk.StringVar(app)
r2y4_spell.set(SLOT_VALUES[0])

r2y4_slot_choise = tk.OptionMenu(
    app, r2y4_slot, *SLOT_VALUES
)
r2y4_slot_choise.grid(row=3, column=11)

r2y4_spell_choise = tk.OptionMenu(
    app, r2y4_spell, *SLOT_VALUES,
)
r2y4_spell_choise.grid(row=3, column=12)


def get_round_spells():
    spell_book = {}
    spell_book['Раунд 1'] = {
        'Ударить!': {
            'slot': r1y1_slot.get().strip(),
            'spell': r1y1_spell.get().strip()
        },
        'Ударить 2й раз!': {
            'slot': r1y2_slot.get().strip(),
            'spell': r1y2_spell.get().strip()
        },
        'Ударить 3й раз!': {
            'slot': r1y3_slot.get().strip(),
            'spell': r1y3_spell.get().strip()
        },
        'Ударить 4й раз!': {
            'slot': r1y4_slot.get().strip(),
            'spell': r1y4_spell.get().strip()
        },
    }
    spell_book['Раунд 2'] = {
        'Ударить!': {
            'slot': r2y1_slot.get().strip(),
            'spell': r2y1_spell.get().strip()
        },
        'Ударить 2й раз!': {
            'slot': r2y2_slot.get().strip(),
            'spell': r2y2_spell.get().strip()
        },
        'Ударить 3й раз!': {
            'slot': r2y3_slot.get().strip(),
            'spell': r2y3_spell.get().strip()
        },
        'Ударить 4й раз!': {
            'slot': r2y4_slot.get().strip(),
            'spell': r2y4_spell.get().strip()
        },
    }
    return spell_book

