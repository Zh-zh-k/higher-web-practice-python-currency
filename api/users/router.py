from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.dependencies import get_current_user
from database import get_db
from domain.users.dto import CreateUserDTO, UpdateUserDTO, UserDTO
from domain.users.models import User
from domain.users.service import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/register',
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user: CreateUserDTO,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)

    existing_user = await service.get_user_by_email(user.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists',
        )

    return await service.create_user(user)


@router.get(
    '/email/{email}',
    response_model=UserDTO,
)
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)

    user = await service.get_user_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    return user


@router.get(
    '/{user_id}',
    response_model=UserDTO,
)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)

    user = await service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    return user


@router.put(
    '',
    response_model=UserDTO,
)
async def update_user(
    user_data: UpdateUserDTO,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)

    updated_user = await service.update_user(
        user_id=current_user.id,
        user_data=user_data,
    )

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    return updated_user
