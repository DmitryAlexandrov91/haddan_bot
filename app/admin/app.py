from dao.models import Event, Preset, SlotSpell, SpellBook, UserAccess
from dao.services import SessionService
from di import resolve
from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import Engine

fast_api_app = FastAPI()
admin = Admin(
    fast_api_app,
    engine=resolve(Engine),
    session_maker=resolve(SessionService).session)


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


class UserAccessAdmin(ModelView, model=UserAccess):
    """Админка модели UserAccess."""

    column_list = [
        UserAccess.id,
        UserAccess.username,
        UserAccess.access,
    ]


admin.add_view(EventAdmin)
admin.add_view(PresetAdmin)
admin.add_view(SpellBookAdmin)
admin.add_view(SloSpellAdmin)
admin.add_view(UserAccessAdmin)
