import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from domain.auth.dto import Token, TokenPayload
from domain.users.service import UserService

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class AuthService:
    ALGORITHM = "HS256"
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key",
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_service = UserService(db)

    def _create_token(
        self,
        user_id: int,
        email: str,
        token_type: str,
        expires_delta: timedelta,
    ) -> str:
        expire = datetime.now(timezone.utc) + expires_delta

        payload = {
            "user_id": user_id,
            "email": email,
            "token_type": token_type,
            "exp": expire,
        }

        return jwt.encode(
            payload,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM,
        )

    async def login(self, email: str, password: str) -> Token:
        """Аутентифицировать пользователя и создать токены.

        :param email: Адрес электронной почты пользователя
        :param password: Пароль в виде обычного текста
        :return: Объект токена с access и refresh токенами
        :raises CredentialsError: Если учетные данные недействительны
        """
        user = await self.user_service.get_user_by_email(email)

        if user is None:
            raise ValueError("Invalid credentials")

        if not password_context.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")

        access_token = self._create_token(
            user_id=user.id,
            email=user.email,
            token_type="access",
            expires_delta=timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )

        refresh_token = self._create_token(
            user_id=user.id,
            email=user.email,
            token_type="refresh",
            expires_delta=timedelta(
                days=self.REFRESH_TOKEN_EXPIRE_DAYS
            ),
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh_tokens(self, refresh_token: str) -> Token:
        """Обновить access токен, используя refresh токен.

        :param refresh_token: Строка refresh токена
        :return: Новый объект токена с обновленными access и refresh токенами
        """
        try:
            payload = jwt.decode(
                refresh_token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM],
            )

            token_payload = TokenPayload(**payload)

        except JWTError:
            raise ValueError("Invalid credentials")

        if token_payload.token_type != "refresh":
            raise ValueError("Invalid credentials")

        user = await self.user_service.get_user_by_id(
            token_payload.user_id
        )

        if user is None:
            raise ValueError("Invalid credentials")

        access_token = self._create_token(
            user_id=user.id,
            email=user.email,
            token_type="access",
            expires_delta=timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )

        new_refresh_token = self._create_token(
            user_id=user.id,
            email=user.email,
            token_type="refresh",
            expires_delta=timedelta(
                days=self.REFRESH_TOKEN_EXPIRE_DAYS
            ),
        )

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )
