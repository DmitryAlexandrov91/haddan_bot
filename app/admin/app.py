from dao.database import sync_engine, sync_session_maker
from dao.models import Event
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


admin.add_view(EventAdmin)
