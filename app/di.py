import punq
from aiogram import Bot
from config import settings


def _inject_tg(container: punq.Container) -> None:
    """Регистрация контейнера."""
    container.register(
        Bot, instance=Bot(
            settings.TELEGRAM_BOT_TOKEN,
        ), scope='singleton',
    )


def create_container() -> punq.Container:
    """Создание контейнера."""
    container = punq.Container()
    _inject_tg(container)
    return container


def resolve[Thing](thing: type[Thing]) -> Thing:
    """Разрешение зависимостей."""
    return container.resolve(thing)  # type: ignore[no-any-return]


container = create_container()
