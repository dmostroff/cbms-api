from datetime import date, datetime
from typing import Optional
from pydantic import field_validator, BaseModel
from pydantic import condecimal
from common.common_service import (
    empty_to_none_or_trim,
    sanitize_float,
    sanitize_date,
    sanitize_datetime,
)


class CreditLineHistoryModel(BaseModel):
    id: Optional[int] = None
    client_id: int
    client_code: str
    card_id: int
    xero_id: str
    cl_date: Optional[date] = None
    amount: Optional[float] = None
    cl_status: None | str = None
    notes: None | str = None
    cl_info: None | str = None
    recorded_on: Optional[datetime] = None

    @field_validator("cl_status", "cl_info", "notes", mode="before")
    @classmethod
    def no_blanks(cls, v):
        return empty_to_none_or_trim(v)

    @field_validator("cl_date", mode="before")
    @classmethod
    def valid_date(cls, v):
        return sanitize_date(v)

    @field_validator("amount", mode="before")
    @classmethod
    def valid_float(cls, v):
        return sanitize_float(v)

    @field_validator("recorded_on", mode="before")
    @classmethod
    def valid_datetime(cls, v):
        return sanitize_datetime(v)
