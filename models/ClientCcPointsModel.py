from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClientCcPointsModel(BaseModel):
    cc_points_id: int
    client_id: int
    cc_account_id: int
    sold_to: str
    sold_on: datetime
    sold_points: Optional[int] = None
    price: Optional[int] = None
    login: Optional[str] = None
    pwd: Optional[str] = None
    source_info: Optional[str] = None
    recorded_on: datetime
