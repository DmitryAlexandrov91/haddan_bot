from datetime import datetime
import pytz

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
        default=lambda: datetime.now(pytz.timezone('Europe/Moscow')),
        doc='Дата и время создания',
    )
