from datetime import datetime, date
from typing import Optional
from pydantic import field_validator, Field, BaseModel
from common.common_service import (
    empty_to_none_or_trim,
    sanitize_float,
    sanitize_date,
    sanitize_datetime,
)
from decimal import Decimal
from typing_extensions import Annotated


class CcAccountModel(BaseModel):
    id: Optional[int] = None
    client_id: int
    xero_id: str
    client_code: None | str = None
    first_name: None | str = None
    last_name: None | str = None
    card_name: str
    card_status: None | str = None
    device: None | str = None
    open_date: Optional[date] = None
    cc_login: None | str = None
    cc_pwd: None | str = None
    cc_card_info: None | str = None
    card_num: None | str = None
    card_exp: None | str = None
    card_cvv: None | str = None
    card_pin: None | str = None
    reconciled_on: Optional[date] = None
    charged_on: Optional[date] = None
    credit_line: Optional[Annotated[Decimal, Field(max_digits=8, decimal_places=2)]] = (
        None
    )
    due_on: Optional[date] = None
    bonus_to_spend: Optional[
        Annotated[Decimal, Field(max_digits=8, decimal_places=2)]
    ] = None
    bonus_spend_by: Optional[date] = None
    bonus_spent: Optional[Annotated[Decimal, Field(max_digits=8, decimal_places=2)]] = (
        None
    )
    ccaccount_info: None | str = None
    task: None | str = None
    in_charge: None | str = None
    notes: None | str = None
    recorded_on: Optional[datetime] = None

    @field_validator(
        "client_code",
        "first_name",
        "last_name",
        "card_status",
        "device",
        "ccaccount_info",
        "task",
        "in_charge",
        "notes",
        mode="before",
    )
    @classmethod
    def no_blanks(cls, v):
        return empty_to_none_or_trim(v)

    @field_validator(
        "open_date",
        "reconciled_on",
        "charged_on",
        "due_on",
        "bonus_spend_by",
        mode="before",
    )
    @classmethod
    def valid_date(cls, v):
        return sanitize_date(v)

    @field_validator("credit_line", "bonus_to_spend", "bonus_spent", mode="before")
    @classmethod
    def valid_float(cls, v):
        return sanitize_float(v)

    @field_validator("recorded_on", mode="before")
    @classmethod
    def valid_datetime(cls, v):
        return sanitize_datetime(v)

    def ensemble_cc_card_info(cls, v):
        return "~".join([cls.card_num, cls.card_exp, cls.card_cvv, cls.card_pin])

    def dissemble_cc_card_info(cls):
        if isinstance(cls.cc_card_info, str):
            if cls.cc_card_info.count("~") == 3:
                [cls.card_num, cls.card_exp, cls.card_cvv, cls.card_pin] = (
                    cls.cc_card_info.split("~")
                )
