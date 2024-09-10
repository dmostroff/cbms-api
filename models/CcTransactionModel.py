from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CcTransactionModel(BaseModel):
    cctrans_id: int
    ccaccount_id: Optional[int] = None
    transaction_date: datetime
    transaction_type: str
    transaction_status: Optional[str] = None
    credit: Optional[int] = None
    debit: Optional[int] = None
    recorded_on: datetime
