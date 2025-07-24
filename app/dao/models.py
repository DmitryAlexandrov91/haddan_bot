from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel


class Event(BaseModel):
    """Модель события."""

    event_name: Mapped[str] = mapped_column(
        String(10),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        doc="Дата и время создания",
    )
