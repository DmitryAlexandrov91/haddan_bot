import functools
import tkinter as tk
from tkinter import messagebox
from typing import Any, Callable

from constants import (
    DEFAULT_SLOT,
    DEFAULT_SLOTS_PAGE,
    SLOT_VALUES,
    Slot,
    SlotsPage,
)
from dao.crud import preset_crud, spell_book_crud
from dao.database import sync_session_maker
from dao.models import Preset, SpellBook

from tk_app.core import app

from .utils import create_update_objects


def sync_slots() -> None:
    """Синххронизирует все заклинания с основным."""
    sync_with_main_spell()


quick_slots_open_btn = tk.Button(
    app,
    text='sync ->',
    width=9,
    bg='#FFF4DC',
    command=sync_slots,
)
quick_slots_open_btn.grid(
    row=0, column=6, sticky='w',
)

#  Кнопки основного заклинания ----------------------------------------
main_slots_page = tk.StringVar(app)
main_slots_page.set(DEFAULT_SLOTS_PAGE)

main_spell_slot = tk.StringVar(app)
main_spell_slot.set(DEFAULT_SLOT)

main_slot_label = tk.OptionMenu(
    app, main_slots_page, *SLOT_VALUES,
)
main_slot_label.grid(row=1, column=5)

main_spell_label = tk.OptionMenu(
    app, main_spell_slot, *SLOT_VALUES,
)
main_spell_label.grid(row=1, column=6)
#  --------------------------------------------------------------------


# Раунд 1 (4 удара) ---------------------------------------------------
for element in range(4):
    widget = tk.Label(
        app,
        text=f'Р1 У{element + 1}',
        bg='#FFF4DC',
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
        bg='#FFF4DC',
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
    app, r2y4_slot, *SLOT_VALUES,
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
        bg='#FFF4DC',
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
        bg='#FFF4DC',
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
        bg='#FFF4DC',
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
        bg='#FFF4DC',
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

# -------------------------------------------------------------


# Общие методы интерфейса быстрых слотов-----------------------
def get_round_spells() -> dict[Any, Any]:
    """Формирует книгу заклинаний."""
    spell_book = {}
    spell_book['Раунд 1'] = {
        'Ударить!': {
            'slot': r1y1_slot.get().strip(),
            'spell': r1y1_spell.get().strip(),
        },
        'Ударить 2й раз!': {
            'slot': r1y2_slot.get().strip(),
            'spell': r1y2_spell.get().strip(),
        },
        'Ударить 3й раз!': {
            'slot': r1y3_slot.get().strip(),
            'spell': r1y3_spell.get().strip(),
        },
        'Ударить 4й раз!': {
            'slot': r1y4_slot.get().strip(),
            'spell': r1y4_spell.get().strip(),
        },
    }
    spell_book['Раунд 2'] = {
        'Ударить!': {
            'slot': r2y1_slot.get().strip(),
            'spell': r2y1_spell.get().strip(),
        },
        'Ударить 2й раз!': {
            'slot': r2y2_slot.get().strip(),
            'spell': r2y2_spell.get().strip(),
        },
        'Ударить 3й раз!': {
            'slot': r2y3_slot.get().strip(),
            'spell': r2y3_spell.get().strip(),
        },
        'Ударить 4й раз!': {
            'slot': r2y4_slot.get().strip(),
            'spell': r2y4_spell.get().strip(),
        },
    }
    spell_book['Раунд 3'] = {
        'Ударить!': {
            'slot': r3y1_slot.get().strip(),
            'spell': r3y1_spell.get().strip(),
        },
        'Ударить 2й раз!': {
            'slot': r3y2_slot.get().strip(),
            'spell': r3y2_spell.get().strip(),
        },
        'Ударить 3й раз!': {
            'slot': r3y3_slot.get().strip(),
            'spell': r3y3_spell.get().strip(),
        },
        'Ударить 4й раз!': {
            'slot': r3y4_slot.get().strip(),
            'spell': r3y4_spell.get().strip(),
        },
    }

    spell_book['Раунд 4'] = {
        'Ударить!': {
            'slot': r4y1_slot.get().strip(),
            'spell': r4y1_spell.get().strip(),
        },
        'Ударить 2й раз!': {
            'slot': r4y2_slot.get().strip(),
            'spell': r4y2_spell.get().strip(),
        },
        'Ударить 3й раз!': {
            'slot': r4y3_slot.get().strip(),
            'spell': r4y3_spell.get().strip(),
        },
        'Ударить 4й раз!': {
            'slot': r4y4_slot.get().strip(),
            'spell': r4y4_spell.get().strip(),
        },
    }
    spell_book['Раунд 5'] = {
        'Ударить!': {
            'slot': r5y1_slot.get().strip(),
            'spell': r5y1_spell.get().strip(),
        },
        'Ударить 2й раз!': {
            'slot': r5y2_slot.get().strip(),
            'spell': r5y2_spell.get().strip(),
        },
        'Ударить 3й раз!': {
            'slot': r5y3_slot.get().strip(),
            'spell': r5y3_spell.get().strip(),
        },
        'Ударить 4й раз!': {
            'slot': r5y4_slot.get().strip(),
            'spell': r5y4_spell.get().strip(),
        },
    }
    spell_book['Раунд 6'] = {
        'Ударить!': {
            'slot': r6y1_slot.get().strip(),
            'spell': r6y1_spell.get().strip(),
        },
        'Ударить 2й раз!': {
            'slot': r6y2_slot.get().strip(),
            'spell': r6y2_spell.get().strip(),
        },
        'Ударить 3й раз!': {
            'slot': r6y3_slot.get().strip(),
            'spell': r6y3_spell.get().strip(),
        },
        'Ударить 4й раз!': {
            'slot': r6y4_slot.get().strip(),
            'spell': r6y4_spell.get().strip(),
        },
    }

    return spell_book


def sync_with_main_spell() -> None:
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


def get_preset_dataset_from_tk(preset_name: str) -> dict[str, Any]:
    """Формирует словарь заклинаний на основании значений окна Tkinter."""
    return {
        'name': preset_name,
        'main_page': main_slots_page.get(),
        'main_slot': main_spell_slot.get(),
        'spell_books': [
            {
                'round_num': '1',
                'kick_num': '1',
                'slot_spells':
                    {
                        'page_num': r1y1_slot.get(),
                        'slot_num': r1y1_spell.get(),
                    },
            },
            {
                'round_num': '1',
                'kick_num': '2',
                'slot_spells':
                    {
                        'page_num': r1y2_slot.get(),
                        'slot_num': r1y2_spell.get(),
                    },
            },
            {
                'round_num': '1',
                'kick_num': '3',
                'slot_spells':
                    {
                        'page_num': r1y3_slot.get(),
                        'slot_num': r1y3_spell.get(),
                    },
            },
            {
                'round_num': '1',
                'kick_num': '4',
                'slot_spells':
                    {
                        'page_num': r1y4_slot.get(),
                        'slot_num': r1y4_spell.get(),
                    },
            },
            {
                'round_num': '2',
                'kick_num': '1',
                'slot_spells':
                    {
                        'page_num': r2y1_slot.get(),
                        'slot_num': r2y1_spell.get(),
                    },
            },
            {
                'round_num': '2',
                'kick_num': '2',
                'slot_spells':
                    {
                        'page_num': r2y2_slot.get(),
                        'slot_num': r2y2_spell.get(),
                    },
            },
            {
                'round_num': '2',
                'kick_num': '3',
                'slot_spells':
                    {
                        'page_num': r2y3_slot.get(),
                        'slot_num': r2y3_spell.get(),
                    },
            },
            {
                'round_num': '2',
                'kick_num': '4',
                'slot_spells':
                    {
                        'page_num': r2y4_slot.get(),
                        'slot_num': r2y4_spell.get(),
                    },
            },
            {
                'round_num': '3',
                'kick_num': '1',
                'slot_spells':
                    {
                        'page_num': r3y1_slot.get(),
                        'slot_num': r3y1_spell.get(),
                    },
            },
            {
                'round_num': '3',
                'kick_num': '2',
                'slot_spells':
                    {
                        'page_num': r3y2_slot.get(),
                        'slot_num': r3y2_spell.get(),
                    },
            },
            {
                'round_num': '3',
                'kick_num': '3',
                'slot_spells':
                    {
                        'page_num': r3y3_slot.get(),
                        'slot_num': r3y3_spell.get(),
                    },
            },
            {
                'round_num': '3',
                'kick_num': '4',
                'slot_spells':
                    {
                        'page_num': r3y4_slot.get(),
                        'slot_num': r3y4_spell.get(),
                    },
            },
            {
                'round_num': '4',
                'kick_num': '1',
                'slot_spells':
                    {
                        'page_num': r4y1_slot.get(),
                        'slot_num': r4y1_spell.get(),
                    },
            },
            {
                'round_num': '4',
                'kick_num': '2',
                'slot_spells':
                    {
                        'page_num': r4y2_slot.get(),
                        'slot_num': r4y2_spell.get(),
                    },

            },
            {
                'round_num': '4',
                'kick_num': '3',
                'slot_spells':
                    {
                        'page_num': r4y3_slot.get(),
                        'slot_num': r4y3_spell.get(),
                    },
            },
            {
                'round_num': '4',
                'kick_num': '4',
                'slot_spells':
                    {
                        'page_num': r4y4_slot.get(),
                        'slot_num': r4y4_spell.get(),
                    },
            },
            {
                'round_num': '5',
                'kick_num': '1',
                'slot_spells':
                    {
                        'page_num': r5y1_slot.get(),
                        'slot_num': r5y1_spell.get(),
                    },
            },
            {
                'round_num': '5',
                'kick_num': '2',
                'slot_spells':
                    {
                        'page_num': r5y2_slot.get(),
                        'slot_num': r5y2_spell.get(),
                    },
            },
            {
                'round_num': '5',
                'kick_num': '3',
                'slot_spells':
                    {
                        'page_num': r5y3_slot.get(),
                        'slot_num': r5y3_spell.get(),
                    },
            },
            {
                'round_num': '5',
                'kick_num': '4',
                'slot_spells':
                    {
                        'page_num': r5y4_slot.get(),
                        'slot_num': r5y4_spell.get(),
                    },
            },
            {
                'round_num': '5',
                'kick_num': '4',
                'slot_spells':
                    {
                        'page_num': r5y4_slot.get(),
                        'slot_num': r5y4_spell.get(),
                    },

            },
            {
                'round_num': '6',
                'kick_num': '1',
                'slot_spells':
                    {
                        'page_num': r6y1_slot.get(),
                        'slot_num': r6y1_spell.get(),
                    },
            },
            {
                'round_num': '6',
                'kick_num': '2',
                'slot_spells':
                    {
                        'page_num': r6y2_slot.get(),
                        'slot_num': r6y2_spell.get(),
                    },
            },
            {
                'round_num': '6',
                'kick_num': '3',
                'slot_spells':
                    {
                        'page_num': r6y3_slot.get(),
                        'slot_num': r6y3_spell.get(),
                    },
            },
            {
                'round_num': '6',
                'kick_num': '4',
                'slot_spells':
                    {
                        'page_num': r6y4_slot.get(),
                        'slot_num': r6y4_spell.get(),
                    },
            },
        ],
    }


def config_tk_preset_from_db_data(
        preset: Preset,
        spell_books: list[SpellBook],
) -> None:
    """Конфигурирует настройки tkinter на основе объектов из БД."""
    main_slots_page.set(preset.main_page)
    main_spell_slot.set(preset.main_slot)

    round_1_data = {
        data.kick_num: data.slot_spell for data in spell_books if (
            data.round_num == '1'
        )
    }

    r1y1_slot.set(round_1_data['1'].page_num)
    r1y1_spell.set(round_1_data['1'].slot_num)
    r1y2_slot.set(round_1_data['2'].page_num)
    r1y2_spell.set(round_1_data['2'].slot_num)
    r1y3_slot.set(round_1_data['3'].page_num)
    r1y3_spell.set(round_1_data['3'].slot_num)
    r1y4_slot.set(round_1_data['4'].page_num)
    r1y4_spell.set(round_1_data['4'].slot_num)

    round_2_data = {
        data.kick_num: data.slot_spell for data in spell_books if (
            data.round_num == '2'
        )
    }

    r2y1_slot.set(round_2_data['1'].page_num)
    r2y1_spell.set(round_2_data['1'].slot_num)
    r2y2_slot.set(round_2_data['2'].page_num)
    r2y2_spell.set(round_2_data['2'].slot_num)
    r2y3_slot.set(round_2_data['3'].page_num)
    r2y3_spell.set(round_2_data['3'].slot_num)
    r2y4_slot.set(round_2_data['4'].page_num)
    r2y4_spell.set(round_2_data['4'].slot_num)

    round_3_data = {
        data.kick_num: data.slot_spell for data in spell_books if (
            data.round_num == '3'
        )
    }

    r3y1_slot.set(round_3_data['1'].page_num)
    r3y1_spell.set(round_3_data['1'].slot_num)
    r3y2_slot.set(round_3_data['2'].page_num)
    r3y2_spell.set(round_3_data['2'].slot_num)
    r3y3_slot.set(round_3_data['3'].page_num)
    r3y3_spell.set(round_3_data['3'].slot_num)
    r3y4_slot.set(round_3_data['4'].page_num)
    r3y4_spell.set(round_3_data['4'].slot_num)

    round_4_data = {
        data.kick_num: data.slot_spell for data in spell_books if (
            data.round_num == '4'
        )
    }

    r4y1_slot.set(round_4_data['1'].page_num)
    r4y1_spell.set(round_4_data['1'].slot_num)
    r4y2_slot.set(round_4_data['2'].page_num)
    r4y2_spell.set(round_4_data['2'].slot_num)
    r4y3_slot.set(round_4_data['3'].page_num)
    r4y3_spell.set(round_4_data['3'].slot_num)
    r4y4_slot.set(round_4_data['4'].page_num)
    r4y4_spell.set(round_4_data['4'].slot_num)

    round_5_data = {
        data.kick_num: data.slot_spell for data in spell_books if (
            data.round_num == '5'
        )
    }

    r5y1_slot.set(round_5_data['1'].page_num)
    r5y1_spell.set(round_5_data['1'].slot_num)
    r5y2_slot.set(round_5_data['2'].page_num)
    r5y2_spell.set(round_5_data['2'].slot_num)
    r5y3_slot.set(round_5_data['3'].page_num)
    r5y3_spell.set(round_5_data['3'].slot_num)
    r5y4_slot.set(round_5_data['4'].page_num)
    r5y4_spell.set(round_5_data['4'].slot_num)

    round_6_data = {
        data.kick_num: data.slot_spell for data in spell_books if (
            data.round_num == '6'
        )
    }

    r6y1_slot.set(round_6_data['1'].page_num)
    r6y1_spell.set(round_6_data['1'].slot_num)
    r6y2_slot.set(round_6_data['2'].page_num)
    r6y2_spell.set(round_6_data['2'].slot_num)
    r6y3_slot.set(round_6_data['3'].page_num)
    r6y3_spell.set(round_6_data['3'].slot_num)
    r6y4_slot.set(round_6_data['4'].page_num)
    r6y4_spell.set(round_6_data['4'].slot_num)


def confirm_and_execute(
        preset_button: tk.Button,
        func: Callable,
) -> Any:
    """Функция - обёртка для выдачи окна подтверждения."""
    text = (
        'Вы уверены что хотите записать текущие слоты'
        f' в пресет {preset_button.cget('text')}?'
    )
    if messagebox.askyesno(message=text):
        func()

# ----------------------------------------------------------------------------


# Пресет Дракон --------------------------------------------------------------
def get_dragon_preset() -> None:
    """Пресет для фарма дракона маг ударами."""
    with sync_session_maker() as session:
        dragon_preset = preset_crud.get_single_filtered(
            session=session,
            name='Дракон',
        )

        if not dragon_preset:
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
            return

        spell_books = spell_book_crud.get_multi_filtered(
            session=session,
            preset_id=dragon_preset.id,

        )

        config_tk_preset_from_db_data(
            preset=dragon_preset,
            spell_books=spell_books,
        )


def create_update_dragon_preset() -> None:
    """Обработка кнопки upd пресета Дракон."""
    preset_data = get_preset_dataset_from_tk(
        preset_name='Дракон',
    )

    create_update_objects(
        data=preset_data,
        main_slots_page=main_slots_page,
        main_spell_slot=main_spell_slot,
    )


dragon_preset_button = tk.Button(
    app,
    text='Дракон',
    bg='#FFF4DC',
    command=get_dragon_preset,
)
dragon_preset_button.grid(
    row=4, column=7,
)

dragon_preset_upd = tk.Button(
    app,
    text='upd',
    width=2,
    bg='#ED9A3B',
    command=lambda: confirm_and_execute(
        preset_button=dragon_preset_button,
        func=functools.partial(create_update_dragon_preset),
    ),
)
dragon_preset_upd.grid(
    row=4, column=8,
)
# ----------------------------------------------------------------------------


# Пресет ЦУ-------------------------------------------------------------------
def get_cy_preset() -> None:
    """Пресет для кача в ЦУ."""
    with sync_session_maker() as session:
        cy_preset = preset_crud.get_single_filtered(
            session=session,
            name='ЦУ',
        )

        if not cy_preset:
            main_slot = SlotsPage._1
            main_spell = Slot._1

            main_slots_page.set(main_slot)
            main_spell_slot.set(main_spell)

            sync_with_main_spell()

            r1y1_slot.set(SlotsPage._3)
            r1y1_spell.set(Slot._1)
            return

        spell_books = spell_book_crud.get_multi_filtered(
            session=session,
            preset_id=cy_preset.id,

        )

        config_tk_preset_from_db_data(
            preset=cy_preset,
            spell_books=spell_books,
        )


def create_update_cy_preset() -> None:
    """Обработка кноки upd пресета ЦУ."""
    preset_data = get_preset_dataset_from_tk(
        preset_name='ЦУ',
    )

    create_update_objects(
        data=preset_data,
        main_slots_page=main_slots_page,
        main_spell_slot=main_spell_slot,
    )


farm_CY_preset_button = tk.Button(
    app,
    text='ЦУ',
    bg='#FFF4DC',
    command=get_cy_preset,
)
farm_CY_preset_button.grid(
    row=4, column=9,
)

farm_CY_preset_upd = tk.Button(
    app,
    text='upd',
    width=2,
    bg='#ED9A3B',
    command=lambda: confirm_and_execute(
        preset_button=farm_CY_preset_button,
        func=functools.partial(create_update_cy_preset),
    ),
)
farm_CY_preset_upd.grid(
    row=4, column=10,
)
# ----------------------------------------------------------------------------


# Пресет Лаб------------------------------------------------------------------
def get_maze_preset() -> None:
    """Пресет для лабиринта."""
    with sync_session_maker() as session:
        cy_preset = preset_crud.get_single_filtered(
            session=session,
            name='Лаб',
        )

        if not cy_preset:
            main_slot = SlotsPage._1
            main_spell = Slot._1

            main_slots_page.set(main_slot)
            main_spell_slot.set(main_spell)

            sync_with_main_spell()

            r1y1_slot.set(SlotsPage._3)
            r1y1_spell.set(Slot._1)
            return

        spell_books = spell_book_crud.get_multi_filtered(
            session=session,
            preset_id=cy_preset.id,

        )

        config_tk_preset_from_db_data(
            preset=cy_preset,
            spell_books=spell_books,
        )


def create_update_maze_preset() -> None:
    """Обработка кноки upd пресета Лаб."""
    preset_data = get_preset_dataset_from_tk(
        preset_name='Лаб',
    )

    create_update_objects(
        data=preset_data,
        main_slots_page=main_slots_page,
        main_spell_slot=main_spell_slot,
    )


maze_preset_button = tk.Button(
    app,
    text='Лаб',
    width=3,
    bg='#FFF4DC',
    command=get_maze_preset,
)
maze_preset_button.grid(
    row=4, column=11,
)
maze_preset_button_upd = tk.Button(
    app,
    text='upd',
    width=2,
    bg='#ED9A3B',
    command=lambda: confirm_and_execute(
        preset_button=maze_preset_button,
        func=functools.partial(create_update_maze_preset),
    ),
)
maze_preset_button_upd.grid(
    row=4, column=12,
)
# ----------------------------------------------------------------------------


# Пресет Берег----------------------------------------------------------------
def get_coast_preset() -> None:
    """Пресет для фарма побережья."""
    with sync_session_maker() as session:
        coast_preset = preset_crud.get_single_filtered(
            session=session,
            name='Берег',
        )

        if not coast_preset:
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
            return

        spell_books = spell_book_crud.get_multi_filtered(
            session=session,
            preset_id=coast_preset.id,

        )

        config_tk_preset_from_db_data(
            preset=coast_preset,
            spell_books=spell_books,
        )


def create_update_coast_preset() -> None:
    """Обработка кноки upd пресета Берег."""
    preset_data = get_preset_dataset_from_tk(
        preset_name='Берег',
    )

    create_update_objects(
        data=preset_data,
        main_slots_page=main_slots_page,
        main_spell_slot=main_spell_slot,
    )


coast_preset_button = tk.Button(
    app,
    text='Берег',
    bg='#FFF4DC',
    command=get_coast_preset,
)
coast_preset_button.grid(
    row=9, column=7,
)

coast_preset_upd_button = tk.Button(
    app,
    text='upd',
    width=2,
    bg='#ED9A3B',
    command=lambda: confirm_and_execute(
        preset_button=coast_preset_button,
        func=functools.partial(create_update_coast_preset),
    ),
)
coast_preset_upd_button.grid(
        row=9, column=8,
)
# ----------------------------------------------------------------------------


# Пресет Берег2---------------------------------------------------------------
def get_coast_preset_2() -> None:
    """Второй пресет для фарма побережья."""
    with sync_session_maker() as session:
        coast_preset = preset_crud.get_single_filtered(
            session=session,
            name='Берег2',
        )

        if not coast_preset:
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

        spell_books = spell_book_crud.get_multi_filtered(
            session=session,
            preset_id=coast_preset.id,

        )

        config_tk_preset_from_db_data(
            preset=coast_preset,
            spell_books=spell_books,
        )


def create_update_coast_preset_2() -> None:
    """Обработка кноки upd второго пресета Берег."""
    preset_data = get_preset_dataset_from_tk(
        preset_name='Берег2',
    )

    create_update_objects(
        data=preset_data,
        main_slots_page=main_slots_page,
        main_spell_slot=main_spell_slot,
    )


coast_preset_button_2 = tk.Button(
    app,
    text='Берег 2',
    bg='#FFF4DC',
    command=get_coast_preset_2,
)
coast_preset_button_2.grid(
    row=14, column=7,
)

coast_preset_upd_button_2 = tk.Button(
    app,
    text='upd',
    width=2,
    bg='#ED9A3B',
    command=lambda: confirm_and_execute(
        preset_button=coast_preset_button_2,
        func=functools.partial(create_update_coast_preset_2),
    ),
)
coast_preset_upd_button_2.grid(
        row=14, column=8,
)
# ----------------------------------------------------------------------------


# Пресет Лес -----------------------------------------------------------------
def get_forest_preset() -> None:
    """Пресет для леса."""
    with sync_session_maker() as session:
        forest_preset = preset_crud.get_single_filtered(
            session=session,
            name='Лес',
        )

        if not forest_preset:

            main_slot = SlotsPage._p
            main_spell = Slot._p

            main_slots_page.set(main_slot)
            main_spell_slot.set(main_spell)

            sync_with_main_spell()

            r1y1_slot.set(SlotsPage._2)
            r1y1_spell.set(Slot._1)
            return

        spell_books = spell_book_crud.get_multi_filtered(
            session=session,
            preset_id=forest_preset.id,

        )

        config_tk_preset_from_db_data(
            preset=forest_preset,
            spell_books=spell_books,
        )


def create_update_forest_preset() -> None:
    """Обработка кноки upd пресета Лес."""
    preset_data = get_preset_dataset_from_tk(
        preset_name='Лес',
    )

    create_update_objects(
        data=preset_data,
        main_slots_page=main_slots_page,
        main_spell_slot=main_spell_slot,
    )


forest_preset_button = tk.Button(
    app,
    text='Леc',
    width=3,
    bg='#FFF4DC',
    command=get_forest_preset,
)
forest_preset_button.grid(
    row=9, column=9,
)

forest_preset_upd_button = tk.Button(
    app,
    text='upd',
    width=2,
    bg='#ED9A3B',
    command=lambda: confirm_and_execute(
        preset_button=forest_preset_button,
        func=functools.partial(create_update_forest_preset),
    ),
)
forest_preset_upd_button.grid(
    row=9, column=10,
)
# ----------------------------------------------------------------------------


# Пресет ДЛ (детский лаб)-----------------------------------------------------
def get_baby_maze_preset() -> None:
    """Пресет для детского лаба."""
    with sync_session_maker() as session:
        baby_maze_preset = preset_crud.get_single_filtered(
            session=session,
            name='ДЛ',
        )

        if not baby_maze_preset:
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
            return

        spell_books = spell_book_crud.get_multi_filtered(
            session=session,
            preset_id=baby_maze_preset.id,

        )

        config_tk_preset_from_db_data(
            preset=baby_maze_preset,
            spell_books=spell_books,
        )


def create_update_baby_maze_preset() -> None:
    """Обработка кноки upd пресета ДЛ."""
    preset_data = get_preset_dataset_from_tk(
        preset_name='ДЛ',
    )

    create_update_objects(
        data=preset_data,
        main_slots_page=main_slots_page,
        main_spell_slot=main_spell_slot,
    )


baby_maze_preset_button = tk.Button(
    app,
    text='ДЛ',
    bg='#FFF4DC',
    command=get_baby_maze_preset,
)
baby_maze_preset_button.grid(
    row=9, column=11,
)

baby_maze_preset_upd_button = tk.Button(
    app,
    text='upd',
    width=2,
    bg='#ED9A3B',
    command=lambda: confirm_and_execute(
        preset_button=baby_maze_preset_button,
        func=functools.partial(get_baby_maze_preset),
    ),
)
baby_maze_preset_upd_button.grid(
    row=9, column=12,
)
# ----------------------------------------------------------------------------
