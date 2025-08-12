"""Основная конфигурация приложения tkinter."""
import tkinter as tk

from PIL import Image, ImageTk
from constants import (  # noqa
    FIRST_CHAR,
    MIN_HP_VALUE,
    PASSWORD,
    TELEGRAM_CHAT_ID,
    USER_CHAR,
    USER_CHAR_ID,
    USER_PASSWORD,
)

from config import configure_logging

from .utils import keys

app = tk.Tk()

app.title("Haddan bot v1.5")
app.bind("<Control-KeyPress>", keys)
app.resizable(False, False)

app.configure(bg='#FFF4DC')
app.wm_attributes('-topmost', True)
img = Image.open('icon.ico')
photo = ImageTk.PhotoImage(img)

app.iconphoto(True, photo)


from tk_app.interface.fight import *  # noqa
from tk_app.interface.forest_passing import *  # noqa
from tk_app.interface.glade_farm import *  # noqa
from tk_app.interface.login import *  # noqa
from tk_app.interface.maze import *  # noqa
from tk_app.interface.events import *  # noqa


def start_app() -> None:
    """Запуск основного окна tkinter."""
    configure_logging()
    # username.insert(  # noqa
    #     0, FIRST_CHAR
    # ) if FIRST_CHAR else None
    password_field.insert(  # noqa
        0, PASSWORD,
    ) if PASSWORD else None
    tg_id_field.insert(  # noqa
        0, TELEGRAM_CHAT_ID,
    ) if TELEGRAM_CHAT_ID else None
    min_hp_field.insert(  # noqa
        0, MIN_HP_VALUE,
    ) if MIN_HP_VALUE else 0
    # username_field.insert(0, USER_CHAR)  # noqa
    # password_field.insert(0, USER_PASSWORD)  # noqa
    # tg_id_field.insert(0, USER_CHAR_ID)  # noqa
    manager.alarm_label = alarm_label  # noqa
    manager.status_label = status_label  # noqa
    manager.info_label = info_label  # noqa
    manager.start_button = maze_passing_start_button  # noqa
    manager.forest_button = forest_farm_start_button  # noqa
    app.mainloop()
