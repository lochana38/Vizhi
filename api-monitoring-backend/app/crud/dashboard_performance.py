from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app.models.endpoint import Endpoint
from app.models.usage_daily_summary import UsageDailySummary


def get_response_time_trend(db: Session, range_days: int = 30) -> list[dict]:
    start_date = date.today() - timedelta(days=range_days)

    rows = (
        db.query(
            UsageDailySummary.usage_date,
            func.avg(UsageDailySummary.avg_response_time_ms).label("avg_response_time_ms"),
        )
        .filter(UsageDailySummary.usage_date >= start_date)
        .group_by(UsageDailySummary.usage_date)
        .order_by(UsageDailySummary.usage_date.asc())
        .all()
    )

    return [
        {"usage_date": row.usage_date, "avg_response_time_ms": float(row.avg_response_time_ms or 0)}
        for row in rows
    ]


def get_slowest_endpoints(db: Session, limit: int = 10) -> list[dict]:
    rows = (
        db.query(
            Endpoint,
            func.avg(UsageDailySummary.avg_response_time_ms).label("avg_response_time_ms"),
            func.max(UsageDailySummary.max_response_time_ms).label("max_response_time_ms"),
        )
        .join(UsageDailySummary, UsageDailySummary.endpoint_id == Endpoint.id)
        .group_by(Endpoint.id)
        .order_by(func.avg(UsageDailySummary.avg_response_time_ms).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "endpoint": row[0],
            "avg_response_time_ms": float(row.avg_response_time_ms or 0),
            "max_response_time_ms": row.max_response_time_ms,
        }
        for row in rows
    ]


def get_bandwidth_usage(db: Session, limit: int = 10) -> list[dict]:
    rows = (
        db.query(
            Endpoint,
            func.sum(UsageDailySummary.total_bandwidth_bytes).label("total_bandwidth_bytes"),
        )
        .join(UsageDailySummary, UsageDailySummary.endpoint_id == Endpoint.id)
        .group_by(Endpoint.id)
        .order_by(func.sum(UsageDailySummary.total_bandwidth_bytes).desc())
        .limit(limit)
        .all()
    )

    return [
        {"endpoint": row[0], "total_bandwidth_bytes": int(row.total_bandwidth_bytes or 0)}
        for row in rows
    ]
