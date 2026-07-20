from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class KPICardsOut(BaseModel):
    total_endpoints: int
    active_endpoints: int
    healthy_endpoints: int
    unhealthy_endpoints: int
    health_score_percentage: float


class TrafficTrendPointOut(BaseModel):
    usage_date: date
    total_calls: int


class HealthDistributionOut(BaseModel):
    healthy: int
    warning: int
    critical: int


class RecentAlertOut(BaseModel):
    alert_type: str
    endpoint_id: int
    severity_or_type: str
    detected_at: datetime
    resolved: bool
    details: Optional[str] = None