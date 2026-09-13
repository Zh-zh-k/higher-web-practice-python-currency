import os
import sys

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from domain.currency.models import Currency, ExchangeRate

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


DATABASE_URL = os.getenv(
    "DATABASE_URL_SYNC",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/currency",
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class DatabasePipeline:
    def process_item(self, item):
        with SessionLocal() as db:
            currency = db.execute(
                select(Currency).where(
                    Currency.code == item["code"]
                )
            ).scalar_one_or_none()

            if currency is None:
                currency = Currency(
                    code=item["code"],
                    name=item["name"],
                )
                db.add(currency)
                db.flush()

            exchange_rate = db.execute(
                select(ExchangeRate).where(
                    ExchangeRate.currency_id == currency.id,
                    ExchangeRate.date == item["date"],
                )
            ).scalar_one_or_none()

            if exchange_rate is None:
                exchange_rate = ExchangeRate(
                    currency_id=currency.id,
                    value=item["value"],
                    nominal=item["nominal"],
                    date=item["date"],
                )
                db.add(exchange_rate)
            else:
                exchange_rate.value = item["value"]
                exchange_rate.nominal = item["nominal"]

            db.commit()

        return item
