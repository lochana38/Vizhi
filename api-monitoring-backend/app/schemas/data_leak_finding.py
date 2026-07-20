from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.data_leak_finding import LeakTypeEnum


class DataLeakFindingBase(BaseModel):
    endpoint_id: int
    leak_type: LeakTypeEnum
    sample_snippet: Optional[str] = None
    resolved: bool = False
    resolved_at: Optional[datetime] = None


class DataLeakFindingCreate(DataLeakFindingBase):
    pass


class DataLeakFindingUpdate(DataLeakFindingBase):
    pass


class DataLeakFindingOut(DataLeakFindingBase):
    id: int
    detected_at: datetime

    class Config:
        from_attributes = True
