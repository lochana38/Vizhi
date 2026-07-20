from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.security_finding import IssueTypeEnum, SeverityEnum


class SecurityFindingBase(BaseModel):
    endpoint_id: int
    issue_type: IssueTypeEnum
    severity: SeverityEnum
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    details: Optional[str] = None


class SecurityFindingCreate(SecurityFindingBase):
    pass


class SecurityFindingUpdate(SecurityFindingBase):
    pass


class SecurityFindingOut(SecurityFindingBase):
    id: int
    detected_at: datetime

    class Config:
        from_attributes = True