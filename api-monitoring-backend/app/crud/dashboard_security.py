from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timezone
from typing import Optional

from app.models.security_finding import SecurityFinding, IssueTypeEnum, SeverityEnum


def get_filtered_findings(
    db: Session,
    severity: Optional[SeverityEnum] = None,
    issue_type: Optional[IssueTypeEnum] = None,
    resolved: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[SecurityFinding]:
    query = db.query(SecurityFinding).options(joinedload(SecurityFinding.endpoint))

    if severity is not None:
        query = query.filter(SecurityFinding.severity == severity)
    if issue_type is not None:
        query = query.filter(SecurityFinding.issue_type == issue_type)
    if resolved is not None:
        query = query.filter(SecurityFinding.resolved == resolved)

    return query.order_by(SecurityFinding.detected_at.desc()).offset(skip).limit(limit).all()


def get_security_summary(db: Session) -> dict:
    total = db.query(SecurityFinding).count()
    high = db.query(SecurityFinding).filter(SecurityFinding.severity == SeverityEnum.high).count()
    medium = db.query(SecurityFinding).filter(SecurityFinding.severity == SeverityEnum.medium).count()
    low = db.query(SecurityFinding).filter(SecurityFinding.severity == SeverityEnum.low).count()
    unresolved = db.query(SecurityFinding).filter(SecurityFinding.resolved == False).count()
    resolved = db.query(SecurityFinding).filter(SecurityFinding.resolved == True).count()

    return {
        "total_findings": total,
        "high_count": high,
        "medium_count": medium,
        "low_count": low,
        "unresolved_count": unresolved,
        "resolved_count": resolved,
    }


def mark_finding_resolved(db: Session, finding_id: int) -> SecurityFinding | None:
    finding = db.query(SecurityFinding).filter(SecurityFinding.id == finding_id).first()
    if finding is None:
        return None

    finding.resolved = True
    finding.resolved_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(finding)
    return finding