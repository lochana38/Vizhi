from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.dashboard_security import SecurityFindingWithEndpointOut, SecuritySummaryOut
from app.models.security_finding import IssueTypeEnum, SeverityEnum
from app.crud import dashboard_security as crud_security

router = APIRouter(prefix="/security", tags=["Dashboard - Security"])


@router.get("/findings", response_model=list[SecurityFindingWithEndpointOut])
def filtered_findings(
    severity: Optional[SeverityEnum] = None,
    issue_type: Optional[IssueTypeEnum] = None,
    resolved: Optional[bool] = None,
    skip: int = 0,
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud_security.get_filtered_findings(
        db, severity=severity, issue_type=issue_type, resolved=resolved, skip=skip, limit=limit
    )


@router.get("/summary", response_model=SecuritySummaryOut)
def security_summary(db: Session = Depends(get_db)):
    return crud_security.get_security_summary(db)


@router.patch("/findings/{finding_id}/resolve", response_model=SecurityFindingWithEndpointOut)
def resolve_finding(finding_id: int, db: Session = Depends(get_db)):
    finding = crud_security.mark_finding_resolved(db, finding_id)
    if finding is None:
        raise HTTPException(status_code=404, detail="Security finding not found")
    return finding