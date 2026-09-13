from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.dependencies import get_current_user
from database import get_db
from domain.currency.dto import CurrencyDTO, ExchangeRateDTO
from domain.currency.service import CurrencyService
from domain.users.models import User

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get(
    "",
    response_model=list[CurrencyDTO],
)
async def list_currencies(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CurrencyService(db)
    return await service.list_currencies()


@router.get(
    "/{currency_code}/history",
    response_model=list[ExchangeRateDTO],
)
async def get_rate_history(
    currency_code: str,
    startdate: date = Query(...),
    enddate: date = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CurrencyService(db)

    rates = await service.get_rate_history(
        target_code=currency_code,
        start_date=startdate,
        end_date=enddate,
    )

    if not rates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Currency not found",
        )

    return rates


@router.get(
    "/{currency_code}/all",
    response_model=list[ExchangeRateDTO],
)
async def get_all_rates(
    currency_code: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CurrencyService(db)

    rates = await service.get_rates_for_currency(currency_code)

    if not rates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Currency not found",
        )

    return rates


@router.get(
    "/{currency_code}",
    response_model=ExchangeRateDTO,
)
async def get_latest_rate(
    currency_code: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CurrencyService(db)

    rate = await service.get_latest_rate(currency_code)

    if rate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Currency not found",
        )

    return rate
