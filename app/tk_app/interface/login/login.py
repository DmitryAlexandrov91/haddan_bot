"""Вход в игру и закрытие бота."""
import threading
import tkinter as tk
from datetime import datetime

from bot_classes import HaddanDriverManager, HaddanUser
from config import settings
from constants import CHARS_ACCESS, DOMENS, DT_FORMAT
from loguru import logger

from tk_app.core import app
from tk_app.driver_manager import manager


def start_login_thread() -> None:
    """Запускает поток с входом в игру."""
    manager.thread = threading.Thread(target=start_game)
    manager.thread.start()


def start_game(manager: HaddanDriverManager = manager) -> None:
    """Запускает игру."""
    try:
        char = username.get().strip()
        password = password_field.get().strip()

        now = datetime.now()
        char_access = CHARS_ACCESS[char]
        if datetime.strptime(
            char_access, DT_FORMAT,
        ) < now:
            manager.send_alarm_message(
                text=(
                    f'Доступ к боту закончился {char_access}, \n'
                    'Обратитесь к администратору.'),
            )
            exit()

        manager.send_status_message(
            text=f'Заходим в игру персонажем {char}',
        )

        manager.domen = DOMENS[domen_url.get()]

        if char and password:
            manager.start_driver()
            manager.user = HaddanUser(
                char=char,
                password=password,
                driver=manager.driver)
            manager.user.login_to_game(
                domen=manager.domen,
            )
            logger.info(
                f"Персонаж {char} зашёл в игру",
            )
            login_to_game.configure(foreground='green')
            manager.clean_label_messages()
            manager.send_status_message('Бот готов к работе')
    except Exception as e:
        logger.error(
            f'\nВозникло исключение {str(e)}\n',
            stack_info=False,
        )


def stop_bot(manager: HaddanDriverManager = manager) -> None:
    """Останавливает цикл."""
    manager.event.clear()
    manager.user.exit_from_game()
    logger.info(
        f"Персонаж {manager.user.char} вышел из игры",
    )
    manager.close_driver()
    login_to_game.configure(foreground='black')
    manager.clean_label_messages()


username_label = tk.Label(app, text='имя', bg='#FFF4DC')
username_label.grid(row=0, column=0, sticky='e')

# username_field = tk.Entry(app, width=25)
# username_field.grid(row=0, column=1)

username = tk.StringVar(app)
username.set(settings.chars_list[0])


username_l = tk.OptionMenu(
    app, username, *settings.chars_list,
)
username_l.configure(
    bg='#FFF4DC',
    activebackground='#FFF4DC',
)
username_l.grid(
    row=0, column=1,
)


password_label = tk.Label(app, text='пароль', bg='#FFF4DC')
password_label.grid(row=1, column=0, sticky='e')

password_field = tk.Entry(app, width=25)
password_field.grid(row=1, column=1)

domen_url = tk.StringVar(app)
domen_url.set(list(DOMENS.keys())[3])

domen_url_label = tk.OptionMenu(
    app, domen_url, *list(DOMENS.keys()),
)
domen_url_label.grid(row=0, column=0, sticky='w')
domen_url_label.configure(
    bg='#FFF4DC',
    activebackground='#FFF4DC',
)


bot_stop_buttton = tk.Button(
    app,
    text='закрыть',
    width=11,
    bg='#FFF4DC',
    command=stop_bot,
    )
bot_stop_buttton.grid(
    row=1, column=2,
)


login_to_game = tk.Button(
    app,
    text='войти',
    width=11,
    bg='#FFF4DC',
    command=start_login_thread,
    )
login_to_game.grid(
    row=0, column=2,
)

# Блок с чекбосом телеграм сообщений и телеграм ID.
send_message_checkbox_value = tk.BooleanVar(value=True)

send_message_check_button = tk.Checkbutton(
    app,
    text="Отправлять сообщения в телеграм",
    variable=send_message_checkbox_value,
    bg='#FFF4DC',
)
send_message_check_button.grid(
    row=0,
    column=4,
    sticky='w',
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
    column=3, columnspan=4,
)

info_label = tk.Label(
    app,
    text='',
    bg='#FFF4DC',
    fg='green')
info_label.grid(
    row=12,
    column=3, columnspan=4,
)

status_label = tk.Label(
    app,
    text='',
    bg='#FFF4DC',
    fg='black')
status_label.grid(
    row=11,
    column=3, columnspan=4,
)
