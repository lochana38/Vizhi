from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DuplicateGroupBase(BaseModel):
    group_label: Optional[str] = None


class DuplicateGroupCreate(DuplicateGroupBase):
    pass


class DuplicateGroupUpdate(DuplicateGroupBase):
    pass


class DuplicateGroupOut(DuplicateGroupBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
