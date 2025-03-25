"""Основная конфигурация приложения tkinter."""
import tkinter as tk

from constants import FIRST_CHAR, PASSWORD
from PIL import Image, ImageTk

from .utils import keys

app = tk.Tk()
app.title("Haddan bot v1.0")
app.bind("<Control-KeyPress>", keys)

app.configure(bg='#FFF4DC')
img = Image.open('icon.ico')
photo = ImageTk.PhotoImage(img)

app.iconphoto(True, photo)

from tk_app.interface.glade_farm import *  # noqa
from tk_app.interface.login import *  # noqa
# from tk_app.interface.fight import *  # noqa


def start_app():
    username_field.insert(0, FIRST_CHAR)
    password_field.insert(0, PASSWORD)
    app.mainloop()
