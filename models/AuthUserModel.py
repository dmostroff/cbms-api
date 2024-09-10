from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class AuthUserModel(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    password_hint: None | str = None
    is_superuser: Optional[bool] = False
    is_staff: Optional[bool] = True
    is_active: Optional[bool] = True
    roles: List[str] | None = None
    created_at: Optional[datetime] = None
