from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class UsageDailySummaryBase(BaseModel):
    endpoint_id: int
    usage_date: date
    total_calls: int = 0
    avg_response_time_ms: Optional[Decimal] = None
    max_response_time_ms: Optional[int] = None
    error_count: int = 0
    total_bandwidth_bytes: int = 0


class UsageDailySummaryCreate(UsageDailySummaryBase):
    pass


class UsageDailySummaryUpdate(UsageDailySummaryBase):
    pass


class UsageDailySummaryOut(UsageDailySummaryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
