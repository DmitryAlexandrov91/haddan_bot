from sqlalchemy.orm import Session

from dao.crud.base import BaseCRUD
from dao.models import Event


class EventCrud(BaseCRUD):
    """Crud класс модели Event."""

    def get_latest(self, session: Session) -> Event | None:
        """Возвращает последнее событие."""
        return (
            session.query(Event)
            .order_by(Event.created_at.desc())
            .first()
        )


event_crud = EventCrud(Event)
