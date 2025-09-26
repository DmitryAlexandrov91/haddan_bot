from config import settings
from dao.services import SessionService
from di import resolve

from app.constants import DT_FORMAT
from app.dao.crud import user_access_crud


def test_char_acces_dict() -> None:
    """Проверка работоспособности загрузки словаря с доступом."""
    with resolve(SessionService)() as session:
        users_access = user_access_crud.get_multi(
            session=session,
        )

        char_access = {
            user.username: user.access.strftime(
                DT_FORMAT) for user in users_access
            }

        assert settings.FIRST_CHAR in char_access.keys()
