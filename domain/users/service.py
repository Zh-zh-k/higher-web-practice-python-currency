from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.users.dto import CreateUserDTO, UpdateUserDTO
from domain.users.models import User

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User:
        """Получить пользователя по адресу электронной почты.

        :param email: Адрес электронной почты пользователя
        :return: Объект модели пользователя
        :raises UserNotFoundError: Если пользователь
        с указанным email не существует
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, id: int) -> User:
        """Получить пользователя по ID.

        :param id: Идентификатор пользователя
        :return: Объект модели пользователя
        :raises UserNotFoundError: Если пользователь
        с указанным ID не существует
        """
        result = await self.db.execute(
            select(User).where(User.id == id)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user: CreateUserDTO) -> User:
        """Создать нового пользователя.

        :param user: Объект передачи данных для создания пользователя
        :return: Созданный объект модели пользователя
        :raises UserAlreadyExistsError: Если пользователь с указанным
        email уже существует
        """
        db_user = User(
            email=user.email,
            password_hash=password_context.hash(user.password),
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user

    async def update_user(
        self,
        user_id: int,
        user_data: UpdateUserDTO,
    ) -> User | None:
        """Обновить существующего пользователя.

        :param user: Объект передачи данных пользователя с паролем
        :return: Обновленный объект модели пользователя
        :raises UserNotFoundError: Если пользователь с указанным
        email не существует
        """
        db_user = await self.get_user_by_id(user_id)

        if db_user is None:
            return None

        if user_data.email is not None:
            db_user.email = user_data.email

        if user_data.password is not None:
            db_user.password_hash = password_context.hash(
                user_data.password
            )

        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user
