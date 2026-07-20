from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.schemas.endpoint import EndpointOut


class ResponseTimeTrendPointOut(BaseModel):
    usage_date: date
    avg_response_time_ms: float


class SlowEndpointOut(BaseModel):
    endpoint: EndpointOut
    avg_response_time_ms: float
    max_response_time_ms: Optional[int] = None


class BandwidthUsageOut(BaseModel):
    endpoint: EndpointOut
    total_bandwidth_bytes: int
