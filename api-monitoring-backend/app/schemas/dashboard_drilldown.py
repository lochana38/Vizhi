from pydantic import BaseModel
from datetime import date
from typing import Optional
from decimal import Decimal

from app.schemas.endpoint import EndpointOut
from app.schemas.security_finding import SecurityFindingOut
from app.schemas.data_leak_finding import DataLeakFindingOut


class EndpointUsagePointOut(BaseModel):
    usage_date: date
    total_calls: int
    avg_response_time_ms: Optional[float] = None


class DuplicateMembershipOut(BaseModel):
    group_id: int
    group_label: Optional[str] = None
    similarity_score: Optional[Decimal] = None


class EndpointDrilldownOut(BaseModel):
    endpoint: EndpointOut
    security_findings: list[SecurityFindingOut]
    data_leak_findings: list[DataLeakFindingOut]
    duplicate_memberships: list[DuplicateMembershipOut]
    usage_timeseries: list[EndpointUsagePointOut]
