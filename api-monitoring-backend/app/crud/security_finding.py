from sqlalchemy.orm import Session
from app.models.security_finding import SecurityFinding
from app.schemas.security_finding import SecurityFindingCreate, SecurityFindingUpdate


def create_security_finding(db: Session, data: SecurityFindingCreate) -> SecurityFinding:
    new_finding = SecurityFinding(**data.model_dump())
    db.add(new_finding)
    db.commit()
    db.refresh(new_finding)
    return new_finding


def get_security_finding(db: Session, finding_id: int) -> SecurityFinding | None:
    return db.query(SecurityFinding).filter(SecurityFinding.id == finding_id).first()


def get_security_findings(db: Session, skip: int = 0, limit: int = 100) -> list[SecurityFinding]:
    return db.query(SecurityFinding).offset(skip).limit(limit).all()


def get_security_findings_by_endpoint(db: Session, endpoint_id: int) -> list[SecurityFinding]:
    return db.query(SecurityFinding).filter(SecurityFinding.endpoint_id == endpoint_id).all()


def update_security_finding(db: Session, finding_id: int, data: SecurityFindingUpdate) -> SecurityFinding | None:
    finding = get_security_finding(db, finding_id)
    if finding is None:
        return None
    for field, value in data.model_dump().items():
        setattr(finding, field, value)
    db.commit()
    db.refresh(finding)
    return finding


def delete_security_finding(db: Session, finding_id: int) -> SecurityFinding | None:
    finding = get_security_finding(db, finding_id)
    if finding is None:
        return None
    db.delete(finding)
    db.commit()
    return finding