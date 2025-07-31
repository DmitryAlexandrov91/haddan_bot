from dao.database import sync_engine, sync_session_maker
from dao.models import Event, Preset, SlotSpell, SpellBook
from fastapi import FastAPI
from sqladmin import Admin, ModelView

app = FastAPI()
admin = Admin(
    app,
    engine=sync_engine,
    session_maker=sync_session_maker,
)


class EventAdmin(ModelView, model=Event):
    """Админка модели Event."""

    column_list = [
        Event.id,
        Event.event_name,
        Event.created_at,
    ]


class PresetAdmin(ModelView, model=Preset):
    """Админка модели Preset."""

    column_list = [
        Preset.id,
        Preset.name,
        Preset.main_page,
        Preset.main_slot,
    ]


class SpellBookAdmin(ModelView, model=SpellBook):
    """Админка модели SpellBook."""

    column_list = [
        SpellBook.id,
        SpellBook.round_num,
        SpellBook.kick_num,
        SpellBook.preset_id,
    ]


class SloSpellAdmin(ModelView, model=SlotSpell):
    """Админка модели SlotSpell."""

    column_list = [
        SlotSpell.id,
        SlotSpell.page_num,
        SlotSpell.slot_num,
        SlotSpell.spell_book_id,
    ]


admin.add_view(EventAdmin)
admin.add_view(PresetAdmin)
admin.add_view(SpellBookAdmin)
admin.add_view(SloSpellAdmin)
