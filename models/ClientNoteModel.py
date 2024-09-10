from datetime import datetime
from typing import Optional
from pydantic import field_validator, BaseModel
from common.common_service import empty_to_none_or_trim, sanitize_int


class ClientNoteModel(BaseModel):
    client_note_id: int
    client_id: int
    note: Optional[str] = None
    tags: Optional[str] = None
    recorded_by: str
    recorded_on: Optional[datetime] = None

    @field_validator("note", mode="before")
    @classmethod
    def valid_note(cls, v):
        return empty_to_none_or_trim(v)

    @field_validator("recorded_by", mode="before")
    @classmethod
    def valid_user(cls, v):
        return -1 if v is None else sanitize_int(v)
