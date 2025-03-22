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

import tk_app.interface.login  # noqa
import tk_app.interface.glade_farm  # noqa


def start_app():
    app.mainloop()
