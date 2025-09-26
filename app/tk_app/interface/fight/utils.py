from tkinter import StringVar

from dao.crud import preset_crud, slot_spell_crud, spell_book_crud
from dao.services import SessionService
from di import resolve


def create_update_objects(
        data: dict,
        main_slots_page: StringVar,
        main_spell_slot: StringVar,
) -> None:
    """Получает / обновляет / создаёт объекты пресета."""
    with resolve(SessionService)() as session:
        preset = preset_crud.get_or_create_or_update(
            session=session,
            name=data['name'],
            main_page=main_slots_page.get(),
            main_slot=main_spell_slot.get(),
        )

        for spell_book_data in data['spell_books']:
            spell_book = spell_book_crud.get_or_create_or_update(
                session=session,
                round_num=spell_book_data['round_num'],
                kick_num=spell_book_data['kick_num'],
                preset_id=preset.id,
                preset=preset,
            )

            slot_spell_crud.get_or_create_or_update(
                session=session,
                page_num=spell_book_data['slot_spells']['page_num'],
                slot_num=spell_book_data['slot_spells']['slot_num'],
                spell_book_id=spell_book.id,
                spell_book=spell_book,
            )
