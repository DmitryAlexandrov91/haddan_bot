from typing import Any

from sqlalchemy.orm import Session

from ..models import Preset
from .base import BaseCRUD


class PresetCrud(BaseCRUD):
    """Crud класс модели Event."""

    def get_spellbook_by_preset_name(
            self,
            session: Session,
            preset_name: str,
    ) -> dict[str, Any] | None:
        """Вытаскивает всю книгу заклинаний по названию пресета."""
        preset = session.query(Preset).filter_by(name=preset_name).first()
        if preset:
            return {
                "preset": preset.name,
                "main_page": preset.main_page,
                "main_slot": preset.main_slot,
                "spell_books": [
                    {
                        "round": sb.round_num,
                        "kick": sb.kick_num,
                        "slots": (
                            sb.slot_spell.page_num,
                            sb.slot_spell.slot_num,
                        ),

                    } for sb in preset.spell_books
                ],
            }
        return None


preset_crud = PresetCrud(Preset)
