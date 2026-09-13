from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from domain.auth.dto import TokenPayload
from domain.auth.service import AuthService
from domain.users.models import User
from domain.users.service import UserService

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            AuthService.SECRET_KEY,
            algorithms=[AuthService.ALGORITHM],
        )

        token_payload = TokenPayload(**payload)

    except (JWTError, ValidationError):
        raise credentials_exception

    if token_payload.token_type != "access":
        raise credentials_exception

    user_service = UserService(db)
    user = await user_service.get_user_by_id(token_payload.user_id)

    if user is None:
        raise credentials_exception

    return user
