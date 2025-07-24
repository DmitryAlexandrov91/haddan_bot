"""Интерфейс прохождение леса."""
import threading
import tkinter as tk

from selenium.common.exceptions import (
    InvalidSessionIdException,
    NoSuchWindowException,
)
from urllib3.exceptions import MaxRetryError

from tk_app.core import app
from tk_app.driver_manager import manager
from tk_app.interface.fight import (
    cheerfulness_drink_checkbox_value,
    cheerfulness_drink_field,
    cheerfulness_slot,
    cheerfulness_spell,
    get_round_spells,
    main_slots_page,
    main_spell_slot,
)
from tk_app.interface.login import (
    send_message_checkbox_value,
    start_login_thread,
    stop_bot,
    tg_id_field,
)


#  Функции фарма леса.
def start_forest_farm() -> None:
    """Точка входа в цикл forest_farm."""
    if not manager.driver:
        manager.send_alarm_message(
            'Сначала войдите в игру!')
        exit()

    manager.start_event()
    forest_farm_start_button.configure(foreground="green")
    manager.send_alarm_message()

    send_message_to_tg = send_message_checkbox_value.get()
    user_telegram_id = tg_id_field.get().strip()

    try:
        manager.send_status_message('Начинаем прохождение леса.')
        manager.forest_passing(
                message_to_tg=send_message_to_tg,
                telegram_id=int(
                    user_telegram_id,
                ) if user_telegram_id else None,
                slots=main_slots_page.get(),
                spell=main_spell_slot.get(),
                spell_book=get_round_spells(),
                cheerfulness=cheerfulness_drink_checkbox_value.get(),
                cheerfulness_min=int(cheerfulness_drink_field.get().strip()),
                cheerfulness_slot=cheerfulness_slot.get(),
                cheerfulness_spell=cheerfulness_spell.get(),
            )
    except (
        InvalidSessionIdException,
        MaxRetryError,
        NoSuchWindowException,
    ):
        manager.send_alarm_message(
            'Драйвер не обнаружен, перезагрузка.',
        )
        stop_forest_farm()
        stop_bot()
        start_login_thread()
        manager.thread.join()
        start_forest_thread()

    finally:
        manager.send_status_message('Бот готов к работе')
        manager.send_alarm_message()


def stop_forest_farm() -> None:
    """Останавливает поток с циклом фарма леса."""
    manager.stop_event()
    if manager.cycle_thread.is_alive():
        manager.send_status_message('Останавливаем фарм поляны')
        manager.send_alarm_message('Дождитесь завершения цикла')
    else:
        manager.send_alarm_message()
        manager.send_status_message(
            'Бот готов к работе',
        ) if manager.driver else manager.send_alarm_message(
            'Игра не запущена',
        )
    forest_farm_start_button.configure(foreground="black")


def start_forest_thread() -> None:
    """Запускает поток с циклом фарма леса."""
    if not manager.cycle_thread or not manager.cycle_thread.is_alive() or (
        not manager.cycle_is_running
    ):
        manager.stop_event()
        manager.cycle_thread = threading.Thread(
            target=start_forest_farm, daemon=True)
        manager.cycle_thread.start()
    else:
        manager.send_alarm_message(
            'Сначала завершите активный цикл!',
        )


#  Кнопки запуска и остановки прохождения леса. ------------------------------
forest_farm_label = tk.Label(
    app,
    text='Прохождение леса',
    bg='#FFF4DC')
forest_farm_label.grid(row=5, column=5, columnspan=2)

forest_farm_start_button = tk.Button(
    app,
    text='старт',
    width=9,
    bg='#FFF4DC',
    command=start_forest_thread,
    )
forest_farm_start_button.grid(
    row=6, column=5,
)

forest_farm_stop_button = tk.Button(
    app,
    text='стоп',
    width=9,
    bg='#FFF4DC',
    command=stop_forest_farm,
    )
forest_farm_stop_button.grid(
    row=6, column=6,
)
#  --------------------------------------------------------------------
