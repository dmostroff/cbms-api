from datetime import datetime, date
from typing import Optional
from pydantic import field_validator, BaseModel
from common.common_service import empty_to_none_or_trim, sanitize_date, sanitize_bool, sanitize_datetime


class CheckingModel(BaseModel):
    id: Optional[int] = None
    client_id: int
    xero_id: str
    xero_main: Optional[bool] = False
    client_code: str
    client_code_additional: None | str = None
    name_on_account: None | str
    account_status: None | str = None
    device: None | str = None
    open_date: Optional[date] = None
    login: None | str = None
    pwd: None | str = None
    bank: None | str = None
    routing: None | str = None
    account: None | str = None
    member_number: None | str = None
    debit_card_num: None | str = None
    debit_card_exp: None | str = None
    debit_card_cvv: None | str = None
    debit_card_pin: None | str = None
    phone_pin: None | str = None
    reconciled_on: Optional[date] = None
    zelle: None | str = None
    wise: Optional[bool] = None
    wise_device: None | str = None
    checking_info: None | str = None
    task: None | str = None
    notes: None | str = None
    recorded_on: Optional[datetime] = None

    @field_validator('client_code', 'client_code_additional', 'name_on_account', 'account_status', 'device', 'routing', 'account', 'member_number'
        , 'debit_card_num', 'debit_card_exp', 'debit_card_cvv', 'debit_card_pin', 'phone_pin'
         ,'zelle', 'wise_device', 'checking_info'
        , 'task', 'notes'
        , mode="before")
    @classmethod
    def no_blanks(cls, v):
        return empty_to_none_or_trim(v)

    @field_validator('open_date', 'reconciled_on', mode="before")
    @classmethod
    def valid_date(cls, v):
        return sanitize_date(v)

    @field_validator( 'xero_main', 'wise', mode="before")
    @classmethod
    def valid_bool(cls, v):
        return sanitize_bool(v)

    @field_validator( 'recorded_on', mode="before")
    @classmethod
    def valid_datetime(cls, v):
        return sanitize_datetime(v)