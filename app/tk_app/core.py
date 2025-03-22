"""Приложение haddan."""
import tkinter as tk

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


def start_app():
    username_field.insert(0, 'SwordS')
    password_field.insert(0, '0>2Z9&vdMPVOV{h')
    app.mainloop()
