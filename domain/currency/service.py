from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.currency.models import Currency, ExchangeRate


class CurrencyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_currencies(self) -> list[Currency]:
        """Получить все доступные валюты.

        :return: Список всех объектов валют
        """
        result = await self.db.execute(
            select(Currency).order_by(Currency.code)
        )
        return list(result.scalars().all())

    async def get_latest_rate(self, target_code: str) -> ExchangeRate | None:
        """Получить последний курс обмена для определенной валюты.

        :param target_code: Код валюты (например, 'USD', 'EUR')
        :return: Последний объект курса обмена или None если не найден
        """
        result = await self.db.execute(
            select(ExchangeRate)
            .join(Currency)
            .where(Currency.code == target_code.upper())
            .order_by(ExchangeRate.date.desc())
            .limit(1)
        )

        return result.scalar_one_or_none()

    async def get_rate_history(
        self,
        target_code: str,
        start_date: date,
        end_date: date,
    ) -> list[ExchangeRate]:
        """Получить исторические курсы обмена для определенной валюты.

        :param target_code: Код валюты (например, 'USD', 'EUR')
        :param start: Дата начала в формате YYYY-MM-DD
        :param end: Дата окончания в формате YYYY-MM-DD
        :return: Список объектов курса обмена за указанный период
        """
        result = await self.db.execute(
            select(ExchangeRate)
            .join(Currency)
            .where(
                Currency.code == target_code.upper(),
                ExchangeRate.date >= start_date,
                ExchangeRate.date <= end_date,
            )
            .order_by(ExchangeRate.date)
        )

        return list(result.scalars().all())

    async def get_rates_for_currency(
        self,
        target_code: str
    ) -> list[ExchangeRate]:
        """Получить все курсы обмена для определенной валюты (полная история).

        :param target_code: Код валюты (например, 'USD', 'EUR')
        :return: Список всех объектов курса обмена для валюты
        """
        result = await self.db.execute(
            select(ExchangeRate)
            .join(Currency)
            .where(Currency.code == target_code.upper())
            .order_by(ExchangeRate.date)
        )

        return list(result.scalars().all())
