from sqlalchemy.orm import Session
from app.models.usage_daily_summary import UsageDailySummary
from app.schemas.usage_daily_summary import UsageDailySummaryCreate, UsageDailySummaryUpdate


def create_summary(db: Session, data: UsageDailySummaryCreate) -> UsageDailySummary:
    new_summary = UsageDailySummary(**data.model_dump())
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    return new_summary


def get_summary(db: Session, summary_id: int) -> UsageDailySummary | None:
    return db.query(UsageDailySummary).filter(UsageDailySummary.id == summary_id).first()


def get_summaries(db: Session, skip: int = 0, limit: int = 100) -> list[UsageDailySummary]:
    return db.query(UsageDailySummary).offset(skip).limit(limit).all()


def get_summaries_by_endpoint(db: Session, endpoint_id: int) -> list[UsageDailySummary]:
    return db.query(UsageDailySummary).filter(UsageDailySummary.endpoint_id == endpoint_id).all()


def update_summary(db: Session, summary_id: int, data: UsageDailySummaryUpdate) -> UsageDailySummary | None:
    summary = get_summary(db, summary_id)
    if summary is None:
        return None
    for field, value in data.model_dump().items():
        setattr(summary, field, value)
    db.commit()
    db.refresh(summary)
    return summary


def delete_summary(db: Session, summary_id: int) -> UsageDailySummary | None:
    summary = get_summary(db, summary_id)
    if summary is None:
        return None
    db.delete(summary)
    db.commit()
    return summary
