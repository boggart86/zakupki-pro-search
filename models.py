from pydantic import BaseModel, Field, field_validator


class SearchParams(BaseModel):
    phrases: str = Field('', alias="phrases")
    excl_phrases: str = Field('', alias="excl-phrases")
    law: list[str] | str = Field('', alias="law")
    purchase_stage: list[str] | str = Field('', alias="purchase-stage")
    price_min: int | str = Field('', alias="price-min")
    price_max: int | str = Field('', alias="price-max")
    date_min: str = Field('', alias="date-min")
    date_max: str = Field('', alias="date-max")
