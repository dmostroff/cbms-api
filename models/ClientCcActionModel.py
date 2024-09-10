from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClientCcActionModel(BaseModel):
    cc_action_id: int
    client_id: int
    cc_account_id: int
    ccaction: Optional[str] = None
    action_type: Optional[str] = None
    action_status: Optional[str] = None
    due_date: Optional[datetime] = None
    details: Optional[str] = None
    recorded_on: datetime
