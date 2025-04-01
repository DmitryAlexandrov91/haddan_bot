"""Основная конфигурация приложения tkinter."""
import tkinter as tk

from constants import (FIRST_CHAR, PASSWORD, TELEGRAM_CHAT_ID, USER_CHAR,
                       USER_CHAR_ID, USER_PASSWORD)
from PIL import Image, ImageTk

from .utils import keys

app = tk.Tk()
app.title("Haddan bot v1.1.1")
app.bind("<Control-KeyPress>", keys)
app.resizable(False, False)

app.configure(bg='#FFF4DC')
img = Image.open('icon.ico')
photo = ImageTk.PhotoImage(img)

app.iconphoto(True, photo)

from tk_app.interface.dev_tests import *  # noqa
from tk_app.interface.fight import *  # noqa
from tk_app.interface.glade_farm import *  # noqa
from tk_app.interface.login import *  # noqa


def start_app():
    # username_field.insert(0, FIRST_CHAR)  # noqa
    # password_field.insert(0, PASSWORD)  # noqa
    # tg_id_field.insert(0, TELEGRAM_CHAT_ID)  # noqa
    # username_field.insert(0, USER_CHAR)  # noqa
    # password_field.insert(0, USER_PASSWORD)  # noqa
    # tg_id_field.insert(0, USER_CHAR_ID)  # noqa
    app.mainloop()
