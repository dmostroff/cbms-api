from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClientCcTransactionModel(BaseModel):
    cc_trans_id: int
    client_id: int
    cc_account_id: int
    transaction_date: datetime
    transaction_type: str
    transaction_status: Optional[str] = None
    credit: Optional[int] = None
    debit: Optional[int] = None
    recorded_on: datetime
