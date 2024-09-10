from datetime import datetime
from typing import Optional
from pydantic import field_validator, BaseModel
from common.common_service import empty_to_none_or_trim, sanitize_datetime


class CreditReportModel(BaseModel):
    id: Optional[int] = None
    client_id: int
    client_code: str
    credit_bureau: str
    login: None | str = None
    pwd: None | str = None
    pin: None | str = None
    recorded_on: Optional[datetime] = None

    @field_validator("credit_bureau", mode="before")
    @classmethod
    def valid_credit_bureau(cls, v):
        retval = empty_to_none_or_trim(v)
        return "Unknown" if retval is None else retval

    @field_validator("login", "pwd", "pin", mode="before")
    @classmethod
    def no_blanks(cls, v):
        return empty_to_none_or_trim(v)

    @field_validator("recorded_on", mode="before")
    @classmethod
    def valid_datetime(cls, v):
        return sanitize_datetime(v)
