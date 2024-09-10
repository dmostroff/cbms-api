from typing import Optional
from pydantic import BaseModel
from models.AdmSettingModel import AdmSettingModel


class AuthRoleModel(BaseModel):
    id: Optional[int] = None
    role: str
    description: None | str = None


class AuthPermissionModel(BaseModel):
    id: Optional[int] = None
    permission: str
    description: None | str = None
    codename: str


class AuthRolePermissionModel(BaseModel):
    id: Optional[int] = None
    role: str
    permission: str


class AuthUserSettingModel(AdmSettingModel):
    user_id: int
