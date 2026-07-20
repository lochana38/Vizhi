from sqlalchemy.orm import Session
from app.models.data_leak_finding import DataLeakFinding
from app.schemas.data_leak_finding import DataLeakFindingCreate, DataLeakFindingUpdate


def create_data_leak_finding(db: Session, data: DataLeakFindingCreate) -> DataLeakFinding:
    new_finding = DataLeakFinding(**data.model_dump())
    db.add(new_finding)
    db.commit()
    db.refresh(new_finding)
    return new_finding


def get_data_leak_finding(db: Session, finding_id: int) -> DataLeakFinding | None:
    return db.query(DataLeakFinding).filter(DataLeakFinding.id == finding_id).first()


def get_data_leak_findings(db: Session, skip: int = 0, limit: int = 100) -> list[DataLeakFinding]:
    return db.query(DataLeakFinding).offset(skip).limit(limit).all()


def get_data_leak_findings_by_endpoint(db: Session, endpoint_id: int) -> list[DataLeakFinding]:
    return db.query(DataLeakFinding).filter(DataLeakFinding.endpoint_id == endpoint_id).all()


def update_data_leak_finding(db: Session, finding_id: int, data: DataLeakFindingUpdate) -> DataLeakFinding | None:
    finding = get_data_leak_finding(db, finding_id)
    if finding is None:
        return None
    for field, value in data.model_dump().items():
        setattr(finding, field, value)
    db.commit()
    db.refresh(finding)
    return finding


def delete_data_leak_finding(db: Session, finding_id: int) -> DataLeakFinding | None:
    finding = get_data_leak_finding(db, finding_id)
    if finding is None:
        return None
    db.delete(finding)
    db.commit()
    return finding
