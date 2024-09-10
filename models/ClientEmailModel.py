from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClientEmailModel(BaseModel):
    id: Optional[int] = None
    client_id: Optional[int] = None
    emailtype: str
    email: str
    isdefault: Optional[bool] = None
    isconfirmed: Optional[bool] = None
    recorded_on: datetime
