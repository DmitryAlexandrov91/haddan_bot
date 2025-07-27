import tkinter as tk

from dao.crud import event_crud
from dao.database import sync_session_maker

from tk_app.core import app

last_forest_pass_label = tk.Label(
    app,
    text="Лес пройден:",
    bg='#FFF4DC',
)
last_forest_pass_label.grid(
    row=14,
    column=0,
)

with sync_session_maker() as session:
    last_event = event_crud.get_single_filtered(
        session=session,
        event_name="Пройден лес",
    )

formatted_time = last_event.created_at.strftime(
    '%d.%m %H:%M:%S',
) if last_event else ""


last_foress_pass_time = tk.Label(
    app,
    text=(
        f'{formatted_time if formatted_time else ""}'
    ),
    bg='#FFF4DC',
)

last_foress_pass_time.grid(
    row=14,
    column=1,
    columnspan=2,
    sticky='w',
)
