"""Основная конфигурация приложения tkinter."""
import platform
import tkinter as tk

from constants import (FIRST_CHAR, MIN_HP_VALUE, PASSWORD,  # noqa
                       TELEGRAM_CHAT_ID, USER_CHAR, USER_CHAR_ID,
                       USER_PASSWORD)
from PIL import Image, ImageTk

from .utils import keys

app = tk.Tk()

app.title("Haddan bot v1.1.2 <stable>")
app.bind("<Control-KeyPress>", keys)
app.resizable(False, False)

# if platform.system() == 'Windows':
#     app.maxsize(773, 500)


app.configure(bg='#FFF4DC')
app.wm_attributes('-topmost', True)
img = Image.open('icon.ico')
photo = ImageTk.PhotoImage(img)

app.iconphoto(True, photo)


from tk_app.interface.dev_code import *  # noqa
from tk_app.interface.fight import *  # noqa
from tk_app.interface.glade_farm import *  # noqa
from tk_app.interface.login import *  # noqa
from tk_app.interface.maze import *  # noqa


def start_app():
    username_field.insert(0, FIRST_CHAR)  # noqa
    password_field.insert(0, PASSWORD)  # noqa
    tg_id_field.insert(0, TELEGRAM_CHAT_ID)  # noqa
    min_hp_field.insert(0, MIN_HP_VALUE)  # noqa
    # username_field.insert(0, USER_CHAR)  # noqa
    # password_field.insert(0, USER_PASSWORD)  # noqa
    # tg_id_field.insert(0, USER_CHAR_ID)  # noqa
    manager.alarm_label = alarm_label  # noqa
    manager.status_label = status_label  # noqa
    manager.info_label = info_label  # noqa
    app.mainloop()
