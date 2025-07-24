"""Валидаторы maze.py"""
from bot_classes import HaddanDriverManager


def send_message_and_stop_cycle(
        message: str,
        manager: HaddanDriverManager) -> None:
    """Отправляет сообщение об ошибке и останавливает цикл."""
    manager.send_alarm_message(text=message)
    manager.stop_event()
    manager.start_button.configure(
        fg='black',
    ) if manager.start_button else None
    exit()
