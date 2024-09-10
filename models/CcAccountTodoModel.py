from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CcAccountTodoModel(BaseModel):
    id: Optional[int] = None
    client_id: int
    cc_account_id: int
    task: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    due_on: Optional[datetime] = None
    recorded_on: Optional[datetime] = None
