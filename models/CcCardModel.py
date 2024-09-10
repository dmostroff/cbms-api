from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CcCardModel(BaseModel):
    id: Optional[int] = None
    cc_company_id: int
    card_name: Optional[str] = None
    version: Optional[str] = None
    annual_fee: Optional[int] = None
    first_year_free: Optional[bool] = None
    recorded_on: datetime
