import tkinter as tk

from constants import LABIRINT_MAP_URL, SLOT_VALUES
from tk_app.core import app
from tk_app.driver_manager import manager


def open_slots():
    current_size = (app.winfo_width(), app.winfo_height())
    min_size = 1490, 552

    if current_size == min_size:
        app.maxsize(current_size[0] + 500, current_size[1])
    else:
        app.maxsize(min_size[0], min_size[1])


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

r1y1_spell = tk.StringVar(app)
r1y1_spell.set(SLOT_VALUES[0])

r1y1_slot = tk.OptionMenu(
    app, r1y1_slot, *SLOT_VALUES,
)
r1y1_slot.grid(row=0, column=8)

r1y1_spell = tk.OptionMenu(
    app, r1y1_spell, *SLOT_VALUES,
)
r1y1_spell.grid(row=0, column=9)

#  Р1 У2
r1y2_slot = tk.StringVar(app)
r1y2_slot.set(SLOT_VALUES[1])

r1y2_spell = tk.StringVar(app)
r1y2_spell.set(SLOT_VALUES[0])

r1y2_slot = tk.OptionMenu(
    app, r1y2_slot, *SLOT_VALUES,
)
r1y2_slot.grid(row=1, column=8)

r1y2_spell = tk.OptionMenu(
    app, r1y2_spell, *SLOT_VALUES,
)
r1y2_spell.grid(row=1, column=9)

#  Р1 У3
r1y3_slot = tk.StringVar(app)
r1y3_slot.set(SLOT_VALUES[1])

r1y3_spell = tk.StringVar(app)
r1y3_spell.set(SLOT_VALUES[0])

r1y3_slot = tk.OptionMenu(
    app, r1y3_slot, *SLOT_VALUES,
)
r1y3_slot.grid(row=2, column=8)

r1y3_spell = tk.OptionMenu(
    app, r1y3_spell, *SLOT_VALUES,
)
r1y3_spell.grid(row=2, column=9)


#  Р1 У4
r1y4_slot = tk.StringVar(app)
r1y4_slot.set(SLOT_VALUES[1])

r1y4_spell = tk.StringVar(app)
r1y4_spell.set(SLOT_VALUES[0])

r1y4_slot = tk.OptionMenu(
    app, r1y4_slot, *SLOT_VALUES,
)
r1y4_slot.grid(row=3, column=8)

r1y4_spell = tk.OptionMenu(
    app, r1y4_spell, *SLOT_VALUES,
)
r1y4_spell.grid(row=3, column=9)


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

r2y1_slot = tk.OptionMenu(
    app, r2y1_slot, *SLOT_VALUES,
)
r2y1_slot.grid(row=0, column=11)

r2y1_spell = tk.OptionMenu(
    app, r2y1_spell, *SLOT_VALUES,
)
r2y1_spell.grid(row=0, column=12)

#  Р2 У2
r2y2_slot = tk.StringVar(app)
r2y2_slot.set(SLOT_VALUES[1])

r2y2_spell = tk.StringVar(app)
r2y2_spell.set(SLOT_VALUES[0])

r2y2_slot = tk.OptionMenu(
    app, r2y2_slot, *SLOT_VALUES,
)
r2y2_slot.grid(row=1, column=11)

r2y2_spell = tk.OptionMenu(
    app, r2y2_spell, *SLOT_VALUES,
)
r2y2_spell.grid(row=1, column=12)

# #  Р2 У3
r2y3_slot = tk.StringVar(app)
r2y3_slot.set(SLOT_VALUES[1])

r2y3_spell = tk.StringVar(app)
r2y3_spell.set(SLOT_VALUES[0])

r2y3_slot = tk.OptionMenu(
    app, r2y3_slot, *SLOT_VALUES,
)
r2y3_slot.grid(row=2, column=11)

r2y3_spell = tk.OptionMenu(
    app, r2y3_spell, *SLOT_VALUES,
)
r2y3_spell.grid(row=2, column=12)

# #  Р2 У4

r2y4_slot = tk.StringVar(app)
r2y4_slot.set(SLOT_VALUES[1])

r2y4_spell = tk.StringVar(app)
r2y4_spell.set(SLOT_VALUES[0])

r2y4_slot = tk.OptionMenu(
    app, r2y4_slot, *SLOT_VALUES
)
r2y4_slot.grid(row=3, column=11)

r2y4_spell = tk.OptionMenu(
    app, r2y4_spell, *SLOT_VALUES,
)
r2y4_spell.grid(row=3, column=12)
