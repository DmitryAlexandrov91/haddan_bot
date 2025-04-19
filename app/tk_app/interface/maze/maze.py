"""Фарм в лабиринте."""
import tkinter as tk

from tk_app.core import app
from tk_app.driver_manager import manager


def start_maze_passing_thread():
    pass


def stop_maze_passing():
    pass


maze_farm_label = tk.Label(
    app,
    text='Прохождение лабиринта ->',
    bg='#FFF4DC'
)
maze_farm_label.grid(row=11, column=0)

maze_passing_start_button = tk.Button(
    app,
    text='старт',
    width=9,
    bg='#FFF4DC',
    command=start_maze_passing_thread
    )
maze_passing_start_button.grid(
    row=11, column=1
)

maze_passing_stop_button = tk.Button(
    app,
    text='стоп',
    width=9,
    bg='#FFF4DC',
    command=stop_maze_passing
    )
maze_passing_stop_button.grid(
    row=11, column=2
)

direct_path_label = tk.Label(
    app,
    text='По прямой в комнату',
    bg='#FFF4DC'
)
direct_path_label.grid(row=12, column=0, sticky='w')

direct_path_field = tk.Entry(
    app, width=4
)
direct_path_field.grid(row=12, column=0, sticky='e')

via_drop_checkbox_value = tk.BooleanVar(value=True)


via_drop_checkbox_button = tk.Checkbutton(
    app,
    text="Через весь дроп",
    variable=via_drop_checkbox_value,
    bg='#FFF4DC'
)
via_drop_checkbox_button.grid(
    row=12,
    column=1,
)
