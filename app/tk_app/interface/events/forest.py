import tkinter as tk

from tk_app.core import app

from dao.crud import event_crud
from dao.database import sync_session_maker


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

    text = event_crud.create(
        session=session,
        event_name="Forest"
    )

last_foress_pass_time = tk.Label(
    app,
    text='Здесь будет время',
    bg='#FFF4DC',
)

last_foress_pass_time.grid(
    row=14,
    column=1,
    columnspan=2
)
