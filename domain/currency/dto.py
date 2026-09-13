from datetime import date

from pydantic import BaseModel, ConfigDict


class CurrencyDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str


class ExchangeRateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    currency_id: int
    value: float
    nominal: int
    date: date
