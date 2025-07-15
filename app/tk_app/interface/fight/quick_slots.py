import tkinter as tk

from constants import (DEFAULT_SLOT, DEFAULT_SLOTS_PAGE, SLOT_VALUES, Slot,
                       SlotsPage)
from tk_app.core import app


def open_slots():
    sync_with_main_spell()


quick_slots_open_btn = tk.Button(
    app,
    text='sync ->',
    width=9,
    bg='#FFF4DC',
    command=open_slots
)
quick_slots_open_btn.grid(
    row=0, column=6, sticky='w'
)

#  Кнопки основного заклинания ----------------------------------------
main_slots_page = tk.StringVar(app)
main_slots_page.set(DEFAULT_SLOTS_PAGE)

main_spell_slot = tk.StringVar(app)
main_spell_slot.set(DEFAULT_SLOT)

main_slot_label = tk.OptionMenu(
    app, main_slots_page, *SLOT_VALUES
)
main_slot_label.grid(row=1, column=5)

main_spell_label = tk.OptionMenu(
    app, main_spell_slot, *SLOT_VALUES,
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
r1y1_slot.set(DEFAULT_SLOTS_PAGE)

r1y1_spell = tk.StringVar(app)
r1y1_spell.set(DEFAULT_SLOT)

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
r1y2_slot.set(DEFAULT_SLOTS_PAGE)

r1y2_spell = tk.StringVar(app)
r1y2_spell.set(DEFAULT_SLOT)

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
r1y3_slot.set(DEFAULT_SLOTS_PAGE)

r1y3_spell = tk.StringVar(app)
r1y3_spell.set(DEFAULT_SLOT)

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
r1y4_slot.set(DEFAULT_SLOTS_PAGE)

r1y4_spell = tk.StringVar(app)
r1y4_spell.set(DEFAULT_SLOT)

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
        text=f'Р2 У{element + 1}',
        bg='#FFF4DC'
    )
    widget.grid(row=0 + element, column=10)

#  Р2 У1

r2y1_slot = tk.StringVar(app)
r2y1_slot.set(DEFAULT_SLOTS_PAGE)

r2y1_spell = tk.StringVar(app)
r2y1_spell.set(DEFAULT_SLOT)

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
r2y2_slot.set(DEFAULT_SLOTS_PAGE)

r2y2_spell = tk.StringVar(app)
r2y2_spell.set(DEFAULT_SLOT)

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
r2y3_slot.set(DEFAULT_SLOTS_PAGE)

r2y3_spell = tk.StringVar(app)
r2y3_spell.set(DEFAULT_SLOT)

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
r2y4_slot.set(DEFAULT_SLOTS_PAGE)

r2y4_spell = tk.StringVar(app)
r2y4_spell.set(DEFAULT_SLOT)

r2y4_slot_choise = tk.OptionMenu(
    app, r2y4_slot, *SLOT_VALUES
)
r2y4_slot_choise.grid(row=3, column=11)

r2y4_spell_choise = tk.OptionMenu(
    app, r2y4_spell, *SLOT_VALUES,
)
r2y4_spell_choise.grid(row=3, column=12)

#  Раунд 3 (4 удара) --------------------------------
for element in range(4):
    widget = tk.Label(
        app,
        text=f'Р3 У{element + 1}',
        bg='#FFF4DC'
    )
    widget.grid(row=5 + element, column=7)

#  Р3 У1
r3y1_slot = tk.StringVar(app)
r3y1_slot.set(DEFAULT_SLOTS_PAGE)

r3y1_spell = tk.StringVar(app)
r3y1_spell.set(DEFAULT_SLOT)

r3y1_slot_choise = tk.OptionMenu(
    app, r3y1_slot, *SLOT_VALUES,
)
r3y1_slot_choise.grid(row=5, column=8)

r3y1_spell_choise = tk.OptionMenu(
    app, r3y1_spell, *SLOT_VALUES,
)
r3y1_spell_choise.grid(row=5, column=9)

#  Р3 У2
r3y2_slot = tk.StringVar(app)
r3y2_slot.set(DEFAULT_SLOTS_PAGE)

r3y2_spell = tk.StringVar(app)
r3y2_spell.set(DEFAULT_SLOT)

r3y2_slot_choise = tk.OptionMenu(
    app, r3y2_slot, *SLOT_VALUES,
)
r3y2_slot_choise.grid(row=6, column=8)

r3y2_spell_choise = tk.OptionMenu(
    app, r3y2_spell, *SLOT_VALUES,
)
r3y2_spell_choise.grid(row=6, column=9)

#  Р3 У3
r3y3_slot = tk.StringVar(app)
r3y3_slot.set(DEFAULT_SLOTS_PAGE)

r3y3_spell = tk.StringVar(app)
r3y3_spell.set(DEFAULT_SLOT)

r3y3_slot_choise = tk.OptionMenu(
    app, r3y3_slot, *SLOT_VALUES,
)
r3y3_slot_choise.grid(row=7, column=8)

r3y3_spell_choise = tk.OptionMenu(
    app, r3y3_spell, *SLOT_VALUES,
)
r3y3_spell_choise.grid(row=7, column=9)

#  Р3 У4
r3y4_slot = tk.StringVar(app)
r3y4_slot.set(DEFAULT_SLOTS_PAGE)

r3y4_spell = tk.StringVar(app)
r3y4_spell.set(DEFAULT_SLOT)

r3y4_slot_choise = tk.OptionMenu(
    app, r3y4_slot, *SLOT_VALUES,
)
r3y4_slot_choise.grid(row=8, column=8)

r3y4_spell_choise = tk.OptionMenu(
    app, r3y4_spell, *SLOT_VALUES,
)
r3y4_spell_choise.grid(row=8, column=9)


#  Раунд 4 (4 удара) --------------------------------
for element in range(4):
    widget = tk.Label(
        app,
        text=f'Р4 У{element + 1}',
        bg='#FFF4DC'
    )
    widget.grid(row=5 + element, column=10)

#  Р4 У1
r4y1_slot = tk.StringVar(app)
r4y1_slot.set(DEFAULT_SLOTS_PAGE)

r4y1_spell = tk.StringVar(app)
r4y1_spell.set(DEFAULT_SLOT)

r4y1_slot_choise = tk.OptionMenu(
    app, r4y1_slot, *SLOT_VALUES,
)
r4y1_slot_choise.grid(row=5, column=11)

r4y1_spell_choise = tk.OptionMenu(
    app, r4y1_spell, *SLOT_VALUES,
)
r4y1_spell_choise.grid(row=5, column=12)

#  Р4 У2
r4y2_slot = tk.StringVar(app)
r4y2_slot.set(DEFAULT_SLOTS_PAGE)

r4y2_spell = tk.StringVar(app)
r4y2_spell.set(DEFAULT_SLOT)

r4y2_slot_choise = tk.OptionMenu(
    app, r4y2_slot, *SLOT_VALUES,
)
r4y2_slot_choise.grid(row=6, column=11)

r4y2_spell_choise = tk.OptionMenu(
    app, r4y2_spell, *SLOT_VALUES,
)
r4y2_spell_choise.grid(row=6, column=12)

#  Р4 У3
r4y3_slot = tk.StringVar(app)
r4y3_slot.set(DEFAULT_SLOTS_PAGE)

r4y3_spell = tk.StringVar(app)
r4y3_spell.set(DEFAULT_SLOT)

r4y3_slot_choise = tk.OptionMenu(
    app, r4y3_slot, *SLOT_VALUES,
)
r4y3_slot_choise.grid(row=7, column=11)

r4y3_spell_choise = tk.OptionMenu(
    app, r4y3_spell, *SLOT_VALUES,
)
r4y3_spell_choise.grid(row=7, column=12)

#  Р4 У4
r4y4_slot = tk.StringVar(app)
r4y4_slot.set(DEFAULT_SLOTS_PAGE)

r4y4_spell = tk.StringVar(app)
r4y4_spell.set(DEFAULT_SLOT)

r4y4_slot_choise = tk.OptionMenu(
    app, r4y4_slot, *SLOT_VALUES,
)
r4y4_slot_choise.grid(row=8, column=11)

r4y4_spell_choise = tk.OptionMenu(
    app, r4y4_spell, *SLOT_VALUES,
)
r4y4_spell_choise.grid(row=8, column=12)

#  Раунд 5 (4 удара) --------------------------------
for element in range(4):
    widget = tk.Label(
        app,
        text=f'Р5 У{element + 1}',
        bg='#FFF4DC'
    )
    widget.grid(row=10 + element, column=7)

#  Р5 У1
r5y1_slot = tk.StringVar(app)
r5y1_slot.set(DEFAULT_SLOTS_PAGE)

r5y1_spell = tk.StringVar(app)
r5y1_spell.set(DEFAULT_SLOT)

r5y1_slot_choise = tk.OptionMenu(
    app, r5y1_slot, *SLOT_VALUES,
)
r5y1_slot_choise.grid(row=10, column=8)

r5y1_spell_choise = tk.OptionMenu(
    app, r5y1_spell, *SLOT_VALUES,
)
r5y1_spell_choise.grid(row=10, column=9)

#  Р5 У2
r5y2_slot = tk.StringVar(app)
r5y2_slot.set(DEFAULT_SLOTS_PAGE)

r5y2_spell = tk.StringVar(app)
r5y2_spell.set(DEFAULT_SLOT)

r5y2_slot_choise = tk.OptionMenu(
    app, r5y2_slot, *SLOT_VALUES,
)
r5y2_slot_choise.grid(row=11, column=8)

r5y2_spell_choise = tk.OptionMenu(
    app, r5y2_spell, *SLOT_VALUES,
)
r5y2_spell_choise.grid(row=11, column=9)

#  Р5 У3
r5y3_slot = tk.StringVar(app)
r5y3_slot.set(DEFAULT_SLOTS_PAGE)

r5y3_spell = tk.StringVar(app)
r5y3_spell.set(DEFAULT_SLOT)

r5y3_slot_choise = tk.OptionMenu(
    app, r5y3_slot, *SLOT_VALUES,
)
r5y3_slot_choise.grid(row=12, column=8)

r5y3_spell_choise = tk.OptionMenu(
    app, r5y3_spell, *SLOT_VALUES,
)
r5y3_spell_choise.grid(row=12, column=9)

#  Р5 У4
r5y4_slot = tk.StringVar(app)
r5y4_slot.set(DEFAULT_SLOTS_PAGE)

r5y4_spell = tk.StringVar(app)
r5y4_spell.set(DEFAULT_SLOT)

r5y4_slot_choise = tk.OptionMenu(
    app, r5y4_slot, *SLOT_VALUES,
)
r5y4_slot_choise.grid(row=13, column=8)

r5y4_spell_choise = tk.OptionMenu(
    app, r5y4_spell, *SLOT_VALUES,
)
r5y4_spell_choise.grid(row=13, column=9)

#  Раунд 6 (4 удара) --------------------------------
for element in range(4):
    widget = tk.Label(
        app,
        text=f'Р6 У{element + 1}',
        bg='#FFF4DC'
    )
    widget.grid(row=10 + element, column=10)

#  Р6 У1
r6y1_slot = tk.StringVar(app)
r6y1_slot.set(DEFAULT_SLOTS_PAGE)

r6y1_spell = tk.StringVar(app)
r6y1_spell.set(DEFAULT_SLOT)

r6y1_slot_choise = tk.OptionMenu(
    app, r6y1_slot, *SLOT_VALUES,
)
r6y1_slot_choise.grid(row=10, column=11)

r6y1_spell_choise = tk.OptionMenu(
    app, r6y1_spell, *SLOT_VALUES,
)
r6y1_spell_choise.grid(row=10, column=12)

#  Р6 У2
r6y2_slot = tk.StringVar(app)
r6y2_slot.set(DEFAULT_SLOTS_PAGE)

r6y2_spell = tk.StringVar(app)
r6y2_spell.set(DEFAULT_SLOT)

r6y2_slot_choise = tk.OptionMenu(
    app, r6y2_slot, *SLOT_VALUES,
)
r6y2_slot_choise.grid(row=11, column=11)

r6y2_spell_choise = tk.OptionMenu(
    app, r6y2_spell, *SLOT_VALUES,
)
r6y2_spell_choise.grid(row=11, column=12)

#  Р6 У3
r6y3_slot = tk.StringVar(app)
r6y3_slot.set(DEFAULT_SLOTS_PAGE)

r6y3_spell = tk.StringVar(app)
r6y3_spell.set(DEFAULT_SLOT)

r6y3_slot_choise = tk.OptionMenu(
    app, r6y3_slot, *SLOT_VALUES,
)
r6y3_slot_choise.grid(row=12, column=11)

r6y3_spell_choise = tk.OptionMenu(
    app, r6y3_spell, *SLOT_VALUES,
)
r6y3_spell_choise.grid(row=12, column=12)

#  Р6 У4
r6y4_slot = tk.StringVar(app)
r6y4_slot.set(DEFAULT_SLOTS_PAGE)

r6y4_spell = tk.StringVar(app)
r6y4_spell.set(DEFAULT_SLOT)

r6y4_slot_choise = tk.OptionMenu(
    app, r6y4_slot, *SLOT_VALUES,
)
r6y4_slot_choise.grid(row=13, column=11)

r6y4_spell_choise = tk.OptionMenu(
    app, r6y4_spell, *SLOT_VALUES,
)
r6y4_spell_choise.grid(row=13, column=12)


def get_round_spells():
    """Формирует книгу заклинаний."""
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
    spell_book['Раунд 3'] = {
        'Ударить!': {
            'slot': r3y1_slot.get().strip(),
            'spell': r3y1_spell.get().strip()
        },
        'Ударить 2й раз!': {
            'slot': r3y2_slot.get().strip(),
            'spell': r3y2_spell.get().strip()
        },
        'Ударить 3й раз!': {
            'slot': r3y3_slot.get().strip(),
            'spell': r3y3_spell.get().strip()
        },
        'Ударить 4й раз!': {
            'slot': r3y4_slot.get().strip(),
            'spell': r3y4_spell.get().strip()
        },
    }

    spell_book['Раунд 4'] = {
        'Ударить!': {
            'slot': r4y1_slot.get().strip(),
            'spell': r4y1_spell.get().strip()
        },
        'Ударить 2й раз!': {
            'slot': r4y2_slot.get().strip(),
            'spell': r4y2_spell.get().strip()
        },
        'Ударить 3й раз!': {
            'slot': r4y3_slot.get().strip(),
            'spell': r4y3_spell.get().strip()
        },
        'Ударить 4й раз!': {
            'slot': r4y4_slot.get().strip(),
            'spell': r4y4_spell.get().strip()
        },
    }
    spell_book['Раунд 5'] = {
        'Ударить!': {
            'slot': r5y1_slot.get().strip(),
            'spell': r5y1_spell.get().strip()
        },
        'Ударить 2й раз!': {
            'slot': r5y2_slot.get().strip(),
            'spell': r5y2_spell.get().strip()
        },
        'Ударить 3й раз!': {
            'slot': r5y3_slot.get().strip(),
            'spell': r5y3_spell.get().strip()
        },
        'Ударить 4й раз!': {
            'slot': r5y4_slot.get().strip(),
            'spell': r5y4_spell.get().strip()
        },
    }
    spell_book['Раунд 6'] = {
        'Ударить!': {
            'slot': r6y1_slot.get().strip(),
            'spell': r6y1_spell.get().strip()
        },
        'Ударить 2й раз!': {
            'slot': r6y2_slot.get().strip(),
            'spell': r6y2_spell.get().strip()
        },
        'Ударить 3й раз!': {
            'slot': r6y3_slot.get().strip(),
            'spell': r6y3_spell.get().strip()
        },
        'Ударить 4й раз!': {
            'slot': r6y4_slot.get().strip(),
            'spell': r6y4_spell.get().strip()
        },
    }

    return spell_book


def sync_with_main_spell():
    """Синхронизирует все слоты с основным ударом."""
    main_slot = main_slots_page.get()
    main_spell = main_spell_slot.get()

    r1y1_slot.set(main_slot)
    r1y1_spell.set(main_spell)
    r1y2_slot.set(main_slot)
    r1y2_spell.set(main_spell)
    r1y3_slot.set(main_slot)
    r1y3_spell.set(main_spell)
    r1y4_slot.set(main_slot)
    r1y4_spell.set(main_spell)

    r2y1_slot.set(main_slot)
    r2y1_spell.set(main_spell)
    r2y2_slot.set(main_slot)
    r2y2_spell.set(main_spell)
    r2y3_slot.set(main_slot)
    r2y3_spell.set(main_spell)
    r2y4_slot.set(main_slot)
    r2y4_spell.set(main_spell)

    r3y1_slot.set(main_slot)
    r3y1_spell.set(main_spell)
    r3y2_slot.set(main_slot)
    r3y2_spell.set(main_spell)
    r3y3_slot.set(main_slot)
    r3y3_spell.set(main_spell)
    r3y4_slot.set(main_slot)
    r3y4_spell.set(main_spell)

    r4y1_slot.set(main_slot)
    r4y1_spell.set(main_spell)
    r4y2_slot.set(main_slot)
    r4y2_spell.set(main_spell)
    r4y3_slot.set(main_slot)
    r4y3_spell.set(main_spell)
    r4y4_slot.set(main_slot)
    r4y4_spell.set(main_spell)

    r5y1_slot.set(main_slot)
    r5y1_spell.set(main_spell)
    r5y2_slot.set(main_slot)
    r5y2_spell.set(main_spell)
    r5y3_slot.set(main_slot)
    r5y3_spell.set(main_spell)
    r5y4_slot.set(main_slot)
    r5y4_spell.set(main_spell)

    r6y1_slot.set(main_slot)
    r6y1_spell.set(main_spell)
    r6y2_slot.set(main_slot)
    r6y2_spell.set(main_spell)
    r6y3_slot.set(main_slot)
    r6y3_spell.set(main_spell)
    r6y4_slot.set(main_slot)
    r6y4_spell.set(main_spell)


sync_button = tk.Button(
    app,
    text='sync',
    bg='#FFF4DC',
    command=sync_with_main_spell
)
# sync_button.grid(
#     row=4, column=10
# )


def get_dragon_preset():
    """Пресет для фарма дракона маг ударами."""
    main_slot = SlotsPage._1
    main_spell = Slot._5

    main_slots_page.set(main_slot)
    main_spell_slot.set(main_spell)

    r1y1_slot.set(SlotsPage._1)
    r1y1_spell.set(Slot._1)
    r1y2_slot.set(SlotsPage._1)
    r1y2_spell.set(Slot._2)
    r1y3_slot.set(SlotsPage._1)
    r1y3_spell.set(Slot._3)
    r1y4_slot.set(main_slot)
    r1y4_spell.set(main_spell)

    r2y1_slot.set(SlotsPage._1)
    r2y1_spell.set(Slot._4)
    r2y2_slot.set(main_slot)
    r2y2_spell.set(main_spell)
    r2y3_slot.set(main_slot)
    r2y3_spell.set(main_spell)
    r2y4_slot.set(main_slot)
    r2y4_spell.set(main_spell)

    r3y1_slot.set(main_slot)
    r3y1_spell.set(main_spell)
    r3y2_slot.set(main_slot)
    r3y2_spell.set(main_spell)
    r3y3_slot.set(main_slot)
    r3y3_spell.set(main_spell)
    r3y4_slot.set(main_slot)
    r3y4_spell.set(main_spell)

    r4y1_slot.set(main_slot)
    r4y1_spell.set(main_spell)
    r4y2_slot.set(main_slot)
    r4y2_spell.set(main_spell)
    r4y3_slot.set(main_slot)
    r4y3_spell.set(main_spell)
    r4y4_slot.set(main_slot)
    r4y4_spell.set(main_spell)

    r5y1_slot.set(main_slot)
    r5y1_spell.set(main_spell)
    r5y2_slot.set(main_slot)
    r5y2_spell.set(main_spell)
    r5y3_slot.set(main_slot)
    r5y3_spell.set(main_spell)
    r5y4_slot.set(main_slot)
    r5y4_spell.set(main_spell)

    r6y1_slot.set(SlotsPage._1)
    r6y1_spell.set(Slot._1)
    r6y2_slot.set(SlotsPage._1)
    r6y2_spell.set(Slot._2)
    r6y3_slot.set(SlotsPage._1)
    r6y3_spell.set(Slot._3)
    r6y4_slot.set(main_slot)
    r6y4_spell.set(main_spell)


dragon_preset = tk.Button(
    app,
    text='Дракон',
    bg='#FFF4DC',
    command=get_dragon_preset
)
dragon_preset.grid(
    row=4, column=8
)


def get_dragon_punch_preset():
    """Пресет для фарма дракона физ ударами."""
    main_slot = SlotsPage._p
    main_spell = Slot._p

    main_slots_page.set(main_slot)
    main_spell_slot.set(main_spell)

    r1y1_slot.set(SlotsPage._1)
    r1y1_spell.set(Slot._1)
    r1y2_slot.set(SlotsPage._1)
    r1y2_spell.set(Slot._2)
    r1y3_slot.set(SlotsPage._1)
    r1y3_spell.set(Slot._3)
    r1y4_slot.set(main_slot)
    r1y4_spell.set(main_spell)

    r2y1_slot.set(SlotsPage._1)
    r2y1_spell.set(Slot._4)
    r2y2_slot.set(main_slot)
    r2y2_spell.set(main_spell)
    r2y3_slot.set(main_slot)
    r2y3_spell.set(main_spell)
    r2y4_slot.set(main_slot)
    r2y4_spell.set(main_spell)

    r3y1_slot.set(main_slot)
    r3y1_spell.set(main_spell)
    r3y2_slot.set(main_slot)
    r3y2_spell.set(main_spell)
    r3y3_slot.set(main_slot)
    r3y3_spell.set(main_spell)
    r3y4_slot.set(main_slot)
    r3y4_spell.set(main_spell)

    r4y1_slot.set(main_slot)
    r4y1_spell.set(main_spell)
    r4y2_slot.set(main_slot)
    r4y2_spell.set(main_spell)
    r4y3_slot.set(main_slot)
    r4y3_spell.set(main_spell)
    r4y4_slot.set(main_slot)
    r4y4_spell.set(main_spell)

    r5y1_slot.set(main_slot)
    r5y1_spell.set(main_spell)
    r5y2_slot.set(main_slot)
    r5y2_spell.set(main_spell)
    r5y3_slot.set(main_slot)
    r5y3_spell.set(main_spell)
    r5y4_slot.set(main_slot)
    r5y4_spell.set(main_spell)

    r6y1_slot.set(SlotsPage._1)
    r6y1_spell.set(Slot._1)
    r6y2_slot.set(SlotsPage._1)
    r6y2_spell.set(Slot._2)
    r6y3_slot.set(SlotsPage._1)
    r6y3_spell.set(Slot._3)
    r6y4_slot.set(main_slot)
    r6y4_spell.set(main_spell)


dragon_punch_preset = tk.Button(
    app,
    text='Дракон ФУ',
    bg='#FFF4DC',
    command=get_dragon_punch_preset
)
dragon_punch_preset.grid(
    row=4, column=10
)


def get_cy_preset():
    """Пресет для кача в ЦУ."""
    main_slot = SlotsPage._1
    main_spell = Slot._1

    main_slots_page.set(main_slot)
    main_spell_slot.set(main_spell)

    sync_with_main_spell()

    r1y1_slot.set(SlotsPage._3)
    r1y1_spell.set(Slot._1)


farm_CY_preset = tk.Button(
    app,
    text='ЦУ',
    bg='#FFF4DC',
    command=get_cy_preset
)
farm_CY_preset.grid(
    row=4, column=12
)


def get_coast_preset():
    """Пресет для фарма побережья."""
    main_slot = SlotsPage._1
    main_spell = Slot._6

    main_slots_page.set(main_slot)
    main_spell_slot.set(main_spell)

    sync_with_main_spell()

    r1y1_slot.set(SlotsPage._3)
    r1y1_spell.set(Slot._1)
    r1y2_slot.set(SlotsPage._3)
    r1y2_spell.set(Slot._4)
    r1y3_slot.set(SlotsPage._1)
    r1y3_spell.set(Slot._1)

    r2y1_slot.set(SlotsPage._1)
    r2y1_spell.set(Slot._3)
    r2y2_slot.set(SlotsPage._1)
    r2y2_spell.set(Slot._4)
    r2y3_slot.set(SlotsPage._1)
    r2y3_spell.set(Slot._2)

    r3y1_slot.set(SlotsPage._1)
    r3y1_spell.set(Slot._3)
    r3y2_slot.set(SlotsPage._1)
    r3y2_spell.set(Slot._4)

    r4y1_slot.set(SlotsPage._1)
    r4y1_spell.set(Slot._3)
    r4y2_slot.set(SlotsPage._1)
    r4y2_spell.set(Slot._4)


farm_coast_preset = tk.Button(
    app,
    text='Берег',
    bg='#FFF4DC',
    command=get_coast_preset
)
farm_coast_preset.grid(
    row=9, column=7
)


def get_coast_preset_2():
    """Пресет для фарма побережья с архангелами."""
    main_slot = SlotsPage._1
    main_spell = Slot._6

    main_slots_page.set(main_slot)
    main_spell_slot.set(main_spell)

    sync_with_main_spell()

    r1y1_slot.set(SlotsPage._2)
    r1y1_spell.set(Slot._1)
    r1y2_slot.set(SlotsPage._2)
    r1y2_spell.set(Slot._1)
    r1y3_slot.set(SlotsPage._2)
    r1y3_spell.set(Slot._1)
    r1y4_slot.set(SlotsPage._1)
    r1y4_spell.set(Slot._1)

    r2y1_slot.set(SlotsPage._3)
    r2y1_spell.set(Slot._1)
    r2y2_slot.set(SlotsPage._1)
    r2y2_spell.set(Slot._1)
    r2y3_slot.set(SlotsPage._1)
    r2y3_spell.set(Slot._2)

    r3y1_slot.set(SlotsPage._1)
    r3y1_spell.set(Slot._2)
    r3y2_slot.set(SlotsPage._1)
    r3y2_spell.set(Slot._4)

    r4y1_slot.set(SlotsPage._1)
    r4y1_spell.set(Slot._3)
    r4y2_slot.set(SlotsPage._1)
    r4y2_spell.set(Slot._4)


farm_coast_preset_2 = tk.Button(
    app,
    text='Берег 2',
    bg='#FFF4DC',
    command=get_coast_preset_2
)
farm_coast_preset_2.grid(
        row=9, column=8
)


def get_baby_maze_preset():
    """Пресет для детского лаба."""
    main_slot = SlotsPage._1
    main_spell = Slot._6

    main_slots_page.set(main_slot)
    main_spell_slot.set(main_spell)

    sync_with_main_spell()

    r1y1_slot.set(SlotsPage._3)
    r1y1_spell.set(Slot._1)
    r1y2_slot.set(SlotsPage._3)
    r1y2_spell.set(Slot._2)
    r1y3_slot.set(SlotsPage._1)
    r1y3_spell.set(Slot._1)

    r2y1_slot.set(SlotsPage._3)
    r2y1_spell.set(Slot._5)
    r2y2_slot.set(SlotsPage._1)
    r2y2_spell.set(Slot._1)
    r2y3_slot.set(SlotsPage._1)
    r2y3_spell.set(Slot._6)

    r3y1_slot.set(SlotsPage._3)
    r3y1_spell.set(Slot._5)

    r4y1_slot.set(SlotsPage._3)
    r4y1_spell.set(Slot._5)

    r5y1_slot.set(SlotsPage._3)
    r5y1_spell.set(Slot._5)

    r6y1_slot.set(SlotsPage._3)
    r6y1_spell.set(Slot._5)


baby_maze_preset = tk.Button(
    app,
    text='ДЛ',
    bg='#FFF4DC',
    command=get_baby_maze_preset
)
baby_maze_preset.grid(
    row=9, column=12
)


def get_forest_nordman():
    """Пресет для леса физом."""
    main_slot = SlotsPage._p
    main_spell = Slot._p

    main_slots_page.set(main_slot)
    main_spell_slot.set(main_spell)

    sync_with_main_spell()

    r1y1_slot.set(SlotsPage._2)
    r1y1_spell.set(Slot._1)


nordman_forest_preset = tk.Button(
    app,
    text='Лес физ',
    bg='#FFF4DC',
    command=get_forest_nordman
)
nordman_forest_preset.grid(
    row=9, column=10
)
