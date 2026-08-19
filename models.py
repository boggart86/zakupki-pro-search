from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

class SearchParams(BaseModel):
    phrases: str | None = Field(None, alias="phrases")
    law: list[str] | None = Field(None, alias="law")
    purchase_stage: list[str] | None = Field(None, alias="purchase-stage")
    price_min: int | None = Field(None, alias="price-min")
    price_max: int | None = Field(None, alias="price-max")
    date_min: str | None = Field(None, alias="date-min")
    date_max: str | None = Field(None, alias="date-max")
    
    @field_validator("*", mode="before")
    @classmethod
    def handle_empty_strings(cls, v):
        """Преобразует пустые строки в None"""
        return None if v == "" or v is None else v

    @field_validator("phrases", mode="after")
    @classmethod
    def split_phrases(cls, v: str | None) -> list[str] | None:
        """
        Разделяет строку по запятой и убирает пробелы
        Возвращает список строк или None
        """
        if v is None:
            return None
        result = [item.strip() for item in v.split(',')]
        return result if result else None



class Lot(BaseModel):
    id: str
    cost: str
    item: str
    customer: str
