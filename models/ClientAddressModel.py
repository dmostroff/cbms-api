from datetime import datetime
from typing import Optional
from pydantic import field_validator, BaseModel
from common.common_service import (
    empty_to_none_or_trim,
    sanitize_bool,
    sanitize_datetime,
)


class ClientAddressModel(BaseModel):
    id: Optional[int] = None
    client_id: Optional[int] = None
    client_code: None | str = None
    street_address: None | str
    city: None | str
    state: None | str
    zip: None | str
    is_current: Optional[bool] = False
    recorded_on: Optional[datetime] = None

    @field_validator("street_address", "city", "state", mode="before")
    @classmethod
    def no_blanks(cls, v):
        return empty_to_none_or_trim(v)

    @field_validator("is_current", mode="before")
    @classmethod
    def valid_bool(cls, v):
        return sanitize_bool(v)

    @field_validator("recorded_on", mode="before")
    @classmethod
    def valid_datetime(cls, v):
        return sanitize_datetime(v)
