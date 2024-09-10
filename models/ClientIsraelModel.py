from datetime import datetime
from typing import Optional
from pydantic import field_validator, BaseModel
from common.common_service import (
    empty_to_none_or_trim,
    sanitize_phone,
    sanitize_datetime,
)


class ClientIsraelModel(BaseModel):
    id: Optional[int] = None
    client_id: Optional[int] = None
    client_code: None | str = None
    bank: None | str = None
    branch: None | str = None
    account: None | str = None
    iban: None | str = None
    iban_name: None | str = None
    address: None | str = None
    city: None | str = None
    zip: None | str = None
    phone: None | str = None
    notes: None | str = None
    recorded_on: Optional[datetime] = None

    @field_validator(
        "bank",
        "branch",
        "account",
        "iban",
        "iban_name",
        "address",
        "city",
        "zip",
        "notes",
        mode="before",
    )
    @classmethod
    def no_blanks(cls, v):
        return empty_to_none_or_trim(v)

    @field_validator("phone", mode="before")
    @classmethod
    def valid_phone(cls, v):
        return sanitize_phone(v)

    @field_validator("recorded_on", mode="before")
    @classmethod
    def valid_datetime(cls, v):
        return sanitize_datetime(v)
