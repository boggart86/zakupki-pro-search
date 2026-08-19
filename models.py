from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class SearchParams(BaseModel):
    phrases: str = Field('', alias="phrases")
    law: list[str] | str = Field(None, alias="law")
    purchase_stage: list[str] | str = Field(None, alias="purchase-stage")
    price_min: int | str = Field(None, alias="price-min")
    price_max: int | str = Field(None, alias="price-max")
    date_min: str = Field(None, alias="date-min")
    date_max: str = Field(None, alias="date-max")

    @field_validator("date_min", "date_max", mode="after")
    @classmethod
    def split_phrases(cls, value: str | None) -> str | None:
        """
        Преобразует дату из формата YYYY-MM-DD в DD.MM.YYYY
        """
        if value is not None:
            try:
                dt = datetime.strptime(value, "%Y-%m-%d")
                return dt.strftime("%d.%m.%Y")
            except ValueError:
                return value  # Если формат не совпадает, возвращаем как есть
