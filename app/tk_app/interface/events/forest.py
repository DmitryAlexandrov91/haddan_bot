import tkinter as tk

from tk_app.core import app

from dao.crud import event_crud
from dao.database import sync_session_maker


last_forest_pass_label = tk.Label(
    app,
    text="Последнее событие:",
    bg='#FFF4DC',
)
last_forest_pass_label.grid(
    row=14,
    column=0,
)

with sync_session_maker() as session:
    last_event = event_crud.get_latest(
        session=session
    )

formatted_time = last_event.created_at.strftime(
    '%d.%m %H:%M:%S'
) if last_event else ""


last_foress_pass_time = tk.Label(
    app,
    text=(
        f'{last_event.event_name if last_event else ""} - '
        f'{formatted_time if formatted_time else ""}'
    ),
    bg='#FFF4DC',
)

last_foress_pass_time.grid(
    row=14,
    column=1,
    columnspan=2
)
