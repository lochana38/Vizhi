from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.endpoint import EndpointOut
from app.models.security_finding import IssueTypeEnum, SeverityEnum


class SecurityFindingWithEndpointOut(BaseModel):
    id: int
    endpoint_id: int
    issue_type: IssueTypeEnum
    severity: SeverityEnum
    detected_at: datetime
    resolved: bool
    resolved_at: Optional[datetime] = None
    details: Optional[str] = None
    endpoint: EndpointOut

    class Config:
        from_attributes = True


class SecuritySummaryOut(BaseModel):
    total_findings: int
    high_count: int
    medium_count: int
    low_count: int
    unresolved_count: int
    resolved_count: int