from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClientCcHistoryModel(BaseModel):
    cc_hist_id: int
    client_id: int
    ccaccount_id: int
    ccevent: str
    ccevent_amt: int
    details: Optional[str] = None
    recorded_on: datetime
