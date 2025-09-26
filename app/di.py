import punq
from aiogram import Bot
from config import settings
from dao.services import SessionService
from sqlalchemy import Engine, create_engine


def _inject_tg(container: punq.Container) -> None:
    """Регистрация контейнера c TG ботом."""
    try:
        container.register(
            Bot,
            instance=Bot(settings.TELEGRAM_BOT_TOKEN),
            scope='singleton',
        )
    except Exception:
        pass


def _inject_database(container: punq.Container) -> None:
    """Регистрация контейнера с базой."""
    container.register(
        Engine,
        instance=create_engine(url=settings.DB_URL),
        )

    container.register(SessionService)


def create_container() -> punq.Container:
    """Создание контейнера."""
    container = punq.Container()
    _inject_tg(container)
    _inject_database(container)
    return container


def resolve[Thing](thing: type[Thing]) -> Thing:
    """Разрешение зависимостей."""
    return container.resolve(thing)  # type: ignore[no-any-return]


container = create_container()
