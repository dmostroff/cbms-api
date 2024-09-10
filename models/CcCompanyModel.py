from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CcCompanyModel(BaseModel):
    id: Optional[int] = None
    company_name: str
    url: Optional[str] = None
    contact: Optional[str] = None
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    phone_2: Optional[str] = None
    phone_cell: Optional[str] = None
    phone_fax: Optional[str] = None
    company_info: Optional[str] = None
    recorded_on: datetime
    