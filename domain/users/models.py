from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from domain.users.constants import (
    EMAIL_MAX_LENGTH,
    PASSWORD_HASH_MAX_LENGTH,
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(EMAIL_MAX_LENGTH),
        unique=True,
        nullable=False,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(
        String(PASSWORD_HASH_MAX_LENGTH),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, "
            f"email={self.email!r})"
        )
