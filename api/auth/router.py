from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from domain.auth.dto import LoginDTO, RefreshTokenDTO, Token
from domain.auth.service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/login',
    response_model=Token,
)
async def login(
    data: LoginDTO,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)

    try:
        return await service.login(
            email=data.email,
            password=data.password,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
        )


@router.post(
    '/refresh',
    response_model=Token,
)
async def refresh(
    data: RefreshTokenDTO,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)

    try:
        return await service.refresh_tokens(
            data.refresh_token
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
        )
