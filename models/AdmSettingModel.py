from typing import Optional
from pydantic import field_validator, BaseModel

class AdmSettingModel(BaseModel):
    id: Optional[int] = None
    prefix: str
    keyname: str
    keyvalue: None | str = None
    display_rank: Optional[int] = None
    
    @field_validator( 'prefix', mode="before")
    @classmethod
    def valid_prefix(cls, v):
        if v is None:
            return '__unknown__'
        v = v.strip() if isinstance( v, str) else str(v)
        return '__unknown__' if v == '' else v

    @field_validator( 'keyname', mode="before")
    @classmethod
    def valid_keyname( cls, v):
        if v is None:
            return '__unknown__'
        v = v.strip() if isinstance( v, str) else str(v)
        return '__unknown__' if v == '' else v

    
    @field_validator( 'display_rank', mode="before")
    @classmethod
    def valid_rank( cls, v):
        return 1 if v is None or v == '' else int(v)
