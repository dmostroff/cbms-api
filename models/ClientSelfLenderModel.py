from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClientSelfLenderModel(BaseModel):
    self_lender_id: int
    client_id: int
    start_date: Optional[datetime] = None
    duration: Optional[int] = None
    pay_from: Optional[str] = None
    monthly_due_date: int
    termination_date: datetime
    login: Optional[str] = None
    pwd: Optional[str] = None
    recorded_on: datetime
