from typing import List

from sqlalchemy.orm import Session

from dao.models import UserAccess


class UserAccessRepo:
    """Репозиторий для операций над моделью UserAccess через DI."""

    def get_multi(
        self,
        session: Session,
    ) -> List[UserAccess]:
        """Получение всех записей."""
        return session.query(UserAccess).all()
