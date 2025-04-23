"""Вход в игру и закрытие бота."""
import logging
import threading
import tkinter as tk

from bot_classes import HaddanUser
from configs import configure_logging
from tk_app.core import app
from tk_app.driver_manager import manager


def start_login_thread():
    manager.thread = threading.Thread(target=start_game)
    manager.thread.start()


def start_game(manager=manager):

    try:
        char = username_field.get().strip()
        password = password_field.get().strip()

        manager.send_status_message(
            text=f'Заходим в игру персонажем {char}'
        )

        if char and password:
            manager.start_driver()
            User = HaddanUser(
                char=char,
                password=password,
                driver=manager.driver)
            User.login_to_game()
            login_to_game.configure(foreground='green')
            manager.clean_label_messages()
            manager.send_status_message('Бот готов к работе')
    except Exception as e:
        configure_logging()
        logging.exception(
            f'\nВозникло исключение {str(e)}\n',
            stack_info=True
        )


def stop_bot(manager=manager):
    manager.event.clear()
    manager.close_driver()
    login_to_game.configure(foreground='black')
    manager.clean_label_messages()


username_label = tk.Label(app, text='имя', bg='#FFF4DC')
username_label.grid(row=0, column=0)

username_field = tk.Entry(app, width=25)
username_field.grid(row=0, column=1)


password_label = tk.Label(app, text='пароль', bg='#FFF4DC')
password_label.grid(row=1, column=0)

password_field = tk.Entry(app, width=25)
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
    command=start_login_thread
    )
login_to_game.grid(
    row=0, column=2
)

# Блок с чекбосом телеграм сообщений и телеграм ID.
send_message_checkbox_value = tk.BooleanVar(value=False)

send_message_check_button = tk.Checkbutton(
    app,
    text="Отправлять сообщения в телеграм",
    variable=send_message_checkbox_value,
    bg='#FFF4DC'
)
send_message_check_button.grid(
    row=0,
    column=4,
    sticky='w'
)

tg_id_field = tk.Entry(app, width=12, justify='center')
tg_id_field.grid(row=1, column=4)

tg_id_label = tk.Label(
    app,
    text='Телеграм ID: ',
    bg='#FFF4DC',
)
tg_id_label.grid(row=1, column=4, sticky='w')


# Лейбл блока уведомлений
alarm_label = tk.Label(
    app,
    text='',
    bg='#FFF4DC',
    fg='red')
alarm_label.grid(
    row=13,
    column=3, columnspan=3
)

info_label = tk.Label(
    app,
    text='',
    bg='#FFF4DC',
    fg='green')
info_label.grid(
    row=12,
    column=3, columnspan=3
)

status_label = tk.Label(
    app,
    text='',
    bg='#FFF4DC',
    fg='black')
status_label.grid(
    row=11,
    column=3, columnspan=3
)
