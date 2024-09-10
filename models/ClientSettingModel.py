from typing import Optional
from pydantic import BaseModel


class ClientSettingModel(BaseModel):
    client_setting_id: int
    client_id: int
    prefix: str
    keyname: str
    keyvalue: Optional[str] = None
