"""Основная конфигурация приложения tkinter."""
import tkinter as tk

from PIL import Image, ImageTk
from config import configure_logging, settings

from tk_app.utils import keys

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

    password_field.insert(  # noqa
        0, settings.HADDAN_PASSWORD,
    )
    tg_id_field.insert(  # noqa
        0, settings.TELEGRAM_CHAT_ID,
    )
    min_hp_field.insert(  # noqa
        0, settings.MIN_HP_VALUE,
    )
    manager.alarm_label = alarm_label  # noqa
    manager.status_label = status_label  # noqa
    manager.info_label = info_label  # noqa
    manager.start_button = maze_passing_start_button  # noqa
    manager.forest_button = forest_farm_start_button  # noqa
    app.mainloop()
