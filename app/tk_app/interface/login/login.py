"""Вход в игру и закрытие бота."""
import threading
import tkinter as tk

from bot_classes import HaddanBot
from tk_app.core import app
from tk_app.driver_manager import manager


def start_thread():
    manager.thread = threading.Thread(target=start_game)
    manager.thread.start()


def start_game(manager=manager):

    char = username_field.get().strip()
    password = password_field.get().strip()

    if char and password:
        manager.start_driver()
        User = HaddanBot(
            char=char,
            password=password,
            driver=manager.driver)
        User.login_to_game()


def stop_bot(manager=manager):
    manager.event.clear()
    manager.close_driver()


username_label = tk.Label(app, text='имя', bg='#FFF4DC')
username_label.grid(row=0, column=0)

username_field = tk.Entry(app, width=30)
username_field.grid(row=0, column=1)


password_label = tk.Label(app, text='пароль', bg='#FFF4DC')
password_label.grid(row=1, column=0)

password_field = tk.Entry(app, width=30)
password_field.grid(row=1, column=1)

bot_stop_buttton = tk.Button(
    app,
    text='закрыть',
    width=11,
    bg='#FFF4DC',
    command=stop_bot
    )
bot_stop_buttton.grid(
    row=1, column=2
)


login_to_game = tk.Button(
    app,
    text='войти',
    width=11,
    bg='#FFF4DC',
    command=start_game
    )
login_to_game.grid(
    row=0, column=2
)
