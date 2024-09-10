from datetime import date, datetime
from typing import Optional
from pydantic import field_validator, BaseModel
from common.common_service import (
    empty_to_none_or_trim,
    sanitize_float,
    sanitize_phone,
    sanitize_date,
    sanitize_datetime,
    sanitize_bool,
)


class ClientPersonModel(BaseModel):
    id: Optional[int] = None
    client_code: str
    last_name: str
    first_name: str
    middle_name: None | str = None
    dob: Optional[date] = None
    ssn: None | str = None
    mmn: None | str = None
    email: None | str = None
    pwd: None | str = None
    occupation: None | str = None
    employer: None | str = None
    income: Optional[float] = None
    phone: None | str = None
    phone_2: None | str = None
    contact_email: None | str = None
    tax_status: None | str = None
    wise: Optional[bool] = None
    client_status: None | str = None
    notes: None | str = None
    client_info: Optional[str] = None
    recorded_on: Optional[datetime] = None

    def dict(self, *args, **kwargs):
        data_dict = super().dict(*args, **kwargs)
        data_dict["dob"] = data_dict["dob"].strftime("%Y-%m-%d")
        data_dict["income"] = str(data_dict["income"])
        return data_dict

    @field_validator(
        "middle_name",
        "ssn",
        "mmn",
        "email",
        "occupation",
        "employer",
        "contact_email",
        "tax_status",
        "client_status",
        "notes",
        mode="before",
    )
    @classmethod
    def no_blanks(cls, v):
        return empty_to_none_or_trim(v)

    @field_validator("dob", mode="before")
    @classmethod
    def valid_date(cls, v):
        return sanitize_date(v)

    @field_validator("income", mode="before")
    @classmethod
    def valid_float(cls, v):
        return sanitize_float(v)

    @field_validator("wise", mode="before")
    @classmethod
    def valid_bool(cls, v):
        return sanitize_bool(v)

    @field_validator("phone", "phone_2", mode="before")
    @classmethod
    def valid_phone(cls, v):
        return sanitize_phone(v)

    @field_validator("client_info", mode="before")
    @classmethod
    def dict_to_string(cls, v):
        if v is None or isinstance(v, str):
            return v
        else:
            return str(v)

    @field_validator("recorded_on", mode="before")
    @classmethod
    def valid_datetime(cls, v):
        return sanitize_datetime(v)
