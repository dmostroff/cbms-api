from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClientCcBalanceTransferModel(BaseModel):
    bal_id: int
    client_id: int
    cc_account_id: int
    due_date: Optional[datetime] = None
    total: Optional[int] = None
    credit_line: Optional[int] = None
    recorded_on: datetime
