from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .database import BaseModel


class SpellBook(BaseModel):

    preset_name: Mapped[str] = mapped_column(
        String(10)
    )
    round: Mapped[str] = mapped_column(
        String(3)
    )
    strike: Mapped[str] = mapped_column(
        String(3)
    )
    slot: Mapped[str] = mapped_column(String(1))
    spell: Mapped[str] = mapped_column(String(1))
