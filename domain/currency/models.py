from datetime import date

from sqlalchemy import (Date, Float, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(
        String(3),
        unique=True,
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    rates: Mapped[list["ExchangeRate"]] = relationship(
        back_populates="currency",
        cascade="all, delete-orphan",
    )


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    __table_args__ = (
        UniqueConstraint(
            "currency_id",
            "date",
            name="uq_currency_rate_date",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    nominal: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    currency: Mapped["Currency"] = relationship(
        back_populates="rates"
    )
