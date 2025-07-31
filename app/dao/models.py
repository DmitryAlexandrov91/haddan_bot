from datetime import datetime
from typing import Optional

import pytz
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel


class Event(BaseModel):
    """Модель события."""

    event_name: Mapped[str] = mapped_column(
        String(30),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.timezone('Europe/Moscow')),
        doc='Дата и время создания',
    )


class Preset(BaseModel):
    """Модель с пресетами заклинаний."""

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="Название пресета",
    )

    spell_books: Mapped[list["SpellBook"]] = relationship(
        back_populates="preset",
        cascade="all, delete-orphan",
    )


class SpellBook(BaseModel):
    """Модель книги заклинаний."""

    round_num: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        comment="Номер раунда",
    )
    kick_num: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        comment="Номер удара",
    )

    preset_id: Mapped[int] = mapped_column(
        ForeignKey("preset.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID связанного пресета",
    )
    preset: Mapped["Preset"] = relationship(
        back_populates="spell_books",
    )

    slot_spells: Mapped[list["SlotSpell"]] = relationship(
        back_populates="spell_book",
        cascade="all, delete-orphan",
    )


class SlotSpell(BaseModel):
    """Модель с номерами страниц слотов и быстрых слотов."""

    page_num: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Номер страницы",
    )

    slot_num: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Номер слота",
    )

    spell_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Название заклинания",
    )

    spell_book_id: Mapped[int] = mapped_column(
        ForeignKey("spellbook.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID связанной книги заклинаний",
    )
    spell_book: Mapped["SpellBook"] = relationship(
        back_populates="slot_spells",
    )
