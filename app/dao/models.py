from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import BaseModel


class Event(BaseModel):

    event_name: Mapped[str] = mapped_column(
        String(10)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        doc="Дата и время создания",
    )
