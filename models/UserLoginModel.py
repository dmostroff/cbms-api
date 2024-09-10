from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserLoginModel(BaseModel):
    id: Optional[int] = None
    username: str
    token: None | str = None
    startpage: None | str = None
    exp_date: Optional[datetime] = None
    recorded_on: Optional[datetime] = None
