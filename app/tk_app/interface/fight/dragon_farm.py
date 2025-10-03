import threading
import tkinter as tk

from selenium.common.exceptions import (
    InvalidSessionIdException,
    NoSuchWindowException,
)
from urllib3.exceptions import MaxRetryError

from tk_app.core import app
from tk_app.driver_manager import manager
from tk_app.interface.fight.quick_slots import (
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


#  Функции фарма драконов.
def start_dragon_farm() -> None:
    """Точка входа в цикл dragon_farm."""
    if not manager.driver:
        manager.send_alarm_message(
            'Сначала войдите в игру!')
        exit()

    manager.send_status_message(
        text='Начинаем фарм дракона',
    )
    dragon_farm_start_button.configure(foreground='green')
    manager.send_alarm_message()

    manager.start_event()
    tg_id = tg_id_field.get().strip()

    try:
        manager.dragon_farm(
            default_slot=main_slots_page.get(),
            default_spell=main_spell_slot.get(),
            spell_book=get_round_spells(),
            message_to_tg=send_message_checkbox_value.get(),
            telegram_id=int(tg_id) if tg_id else None,
        )

    except (
        InvalidSessionIdException,
        MaxRetryError,
        NoSuchWindowException,
    ):
        manager.send_alarm_message(
            'Драйвер не обнаружен, перезагрузка.',
        )
        stop_dragon_farm()
        stop_bot()
        start_login_thread()
        manager.thread.join()
        start_dragon_thread()

    finally:
        manager.send_alarm_message()
        manager.send_status_message('Бот готов к работе')


def stop_dragon_farm() -> None:
    """Останалвивает поток с циклом фарма дракона."""
    manager.stop_event()
    if manager.cycle_thread.is_alive():
        manager.send_status_message('Останавливаем фарм драконов')
        manager.send_alarm_message('Дождитесь завершения цикла')
    else:
        manager.send_alarm_message()
        manager.send_status_message(
            'Бот готов к работе',
        ) if manager.driver else manager.send_alarm_message(
            'Игра не запущена',
        )
    dragon_farm_start_button.configure(foreground='black')


def start_dragon_thread() -> None:
    """Запускает потом с циклом фарма дракона."""
    if not manager.cycle_thread or not manager.cycle_thread.is_alive():
        manager.stop_event()
        manager.cycle_thread = threading.Thread(
            target=start_dragon_farm, daemon=True)
        manager.cycle_thread.start()
    else:
        manager.send_alarm_message(
            'Сначала завершите активный цикл!',
        )


#  Кнопки запуска и остановки фарма драконов. --------------------------------
dragon_farm_label = tk.Label(
    app,
    text='Фарм драконов',
    bg='#FFF4DC')
dragon_farm_label.grid(row=3, column=5, columnspan=2)

dragon_farm_start_button = tk.Button(
    app,
    text='старт',
    width=9,
    bg='#FFF4DC',
    command=start_dragon_thread,
    )
dragon_farm_start_button.grid(
    row=4, column=5,
)

dragon_farm_stop_button = tk.Button(
    app,
    text='стоп',
    width=9,
    bg='#FFF4DC',
    command=stop_dragon_farm,
    )
dragon_farm_stop_button.grid(
    row=4, column=6,
)
#  --------------------------------------------------------------------
