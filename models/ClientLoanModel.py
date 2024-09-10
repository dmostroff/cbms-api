from datetime import datetime, date
from typing import Optional
from pydantic import field_validator, Field, BaseModel
from common.common_service import empty_to_none_or_trim, sanitize_float
from common.common_service import sanitize_date
from decimal import Decimal
from typing_extensions import Annotated


class ClientLoanModel(BaseModel):
    id: Optional[int] = None
    client_id: int
    xero_id: str
    client_code: str
    first_name: None | str = None
    last_name: None | str = None
    card_name: None | str = None
    loan_status: None | str = None
    device: None | str = None
    open_date: Optional[date] = None
    login: None | str = None
    pwd: None | str = None
    loan_number: None | str = None
    reconciled_on: Optional[date] = None
    credit_line: Annotated[Decimal, Field(max_digits=8, decimal_places=2)]
    autopay_account: None | str = None
    due_on: Optional[date] = None
    loan_type: None | str = None
    maturity_on: Optional[date] = None
    loan_info: None | str = None
    task: None | str = None
    notes: None | str = None
    recorded_on: Optional[datetime] = None

    @field_validator(
        "first_name",
        "last_name",
        "card_name",
        "loan_status",
        "device",
        "loan_number",
        "autopay_account",
        "loan_type",
        "loan_info",
        "task",
        "notes",
        mode="before",
    )
    @classmethod
    def no_blanks(cls, v):
        return empty_to_none_or_trim(v)

    @field_validator(
        "open_date", "reconciled_on", "due_on", "maturity_on", mode="before"
    )
    @classmethod
    def valid_date(cls, v):
        return sanitize_date(v)

    @field_validator("credit_line", mode="before")
    @classmethod
    def valid_float(cls, v):
        return sanitize_float(v)
