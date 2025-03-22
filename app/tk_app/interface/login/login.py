import tkinter as tk

from tk_app.core import app

from bot_classes import HaddanBot

from tk_app.driver_manager import manager


def start_game(manager=manager):

    # username_field.


    char = username_field.get().strip()
    password = password_field.get().strip()



    if char and password:
        manager.start_driver()
        User = HaddanBot(
            char=char,
            password=password,
            driver=manager.driver)
        User.login_to_game()


username_label = tk.Label(app, text='имя', bg='#FFF4DC')
username_label.grid(row=0, column=0)

username_field = tk.Entry(app, width=30)
username_field.grid(row=0, column=1)


password_label = tk.Label(app, text='пароль', bg='#FFF4DC')
password_label.grid(row=1, column=0)

password_field = tk.Entry(app, width=30)
password_field.grid(row=1, column=1)


login_to_game = tk.Button(
    app,
    text='Войти в игру',
    width=9,
    bg='#FFF4DC',
    command=start_game
    )
login_to_game.grid(
    row=0, column=2
)
