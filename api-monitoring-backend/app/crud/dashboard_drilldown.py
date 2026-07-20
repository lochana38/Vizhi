from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app.models.endpoint import Endpoint
from app.models.security_finding import SecurityFinding
from app.models.data_leak_finding import DataLeakFinding
from app.models.duplicate_group_member import DuplicateGroupMember
from app.models.duplicate_group import DuplicateGroup
from app.models.usage_daily_summary import UsageDailySummary


def get_endpoint_usage_timeseries(db: Session, endpoint_id: int, range_days: int = 30) -> list[dict]:
    start_date = date.today() - timedelta(days=range_days)

    rows = (
        db.query(UsageDailySummary)
        .filter(
            UsageDailySummary.endpoint_id == endpoint_id,
            UsageDailySummary.usage_date >= start_date,
        )
        .order_by(UsageDailySummary.usage_date.asc())
        .all()
    )

    return [
        {
            "usage_date": row.usage_date,
            "total_calls": row.total_calls or 0,
            "avg_response_time_ms": float(row.avg_response_time_ms) if row.avg_response_time_ms is not None else None,
        }
        for row in rows
    ]


def get_endpoint_full_detail(db: Session, endpoint_id: int, range_days: int = 30) -> dict | None:
    endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if endpoint is None:
        return None

    security_findings = (
        db.query(SecurityFinding)
        .filter(SecurityFinding.endpoint_id == endpoint_id)
        .order_by(SecurityFinding.detected_at.desc())
        .all()
    )

    data_leak_findings = (
        db.query(DataLeakFinding)
        .filter(DataLeakFinding.endpoint_id == endpoint_id)
        .order_by(DataLeakFinding.detected_at.desc())
        .all()
    )

    membership_rows = (
        db.query(DuplicateGroupMember, DuplicateGroup)
        .join(DuplicateGroup, DuplicateGroup.id == DuplicateGroupMember.group_id)
        .filter(DuplicateGroupMember.endpoint_id == endpoint_id)
        .all()
    )
    duplicate_memberships = [
        {
            "group_id": group.id,
            "group_label": group.group_label,
            "similarity_score": member.similarity_score,
        }
        for member, group in membership_rows
    ]

    usage_timeseries = get_endpoint_usage_timeseries(db, endpoint_id, range_days)

    return {
        "endpoint": endpoint,
        "security_findings": security_findings,
        "data_leak_findings": data_leak_findings,
        "duplicate_memberships": duplicate_memberships,
        "usage_timeseries": usage_timeseries,
    }
