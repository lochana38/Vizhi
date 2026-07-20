from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class DuplicateGroupMemberBase(BaseModel):
    group_id: int
    endpoint_id: int
    similarity_score: Optional[Decimal] = None


class DuplicateGroupMemberCreate(DuplicateGroupMemberBase):
    pass


class DuplicateGroupMemberUpdate(DuplicateGroupMemberBase):
    pass


class DuplicateGroupMemberOut(DuplicateGroupMemberBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
