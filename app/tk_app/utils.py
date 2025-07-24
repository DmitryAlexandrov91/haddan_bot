import ctypes
from typing import Any


def is_ru_lang_keyboard() -> Any:
    """Функция для буфера обмена на англ. языке."""
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    return hex(pf(0)) == '0x4190419'


def keys(event: Any) -> None:
    """Функция для буфера обмена на англ. языке."""
    if is_ru_lang_keyboard():
        if event.keycode == 86:
            event.widget.event_generate("<<Paste>>")
        elif event.keycode == 67:
            event.widget.event_generate("<<Copy>>")
        elif event.keycode == 88:
            event.widget.event_generate("<<Cut>>")
        elif event.keycode == 65535:
            event.widget.event_generate("<<Clear>>")
        elif event.keycode == 65:
            event.widget.event_generate("<<SelectAll>>")
