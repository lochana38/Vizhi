from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app.models.endpoint import Endpoint
from app.models.security_finding import SecurityFinding, SeverityEnum
from app.models.data_leak_finding import DataLeakFinding
from app.models.usage_daily_summary import UsageDailySummary


def get_kpi_cards(db: Session) -> dict:
    total_endpoints = db.query(Endpoint).count()
    active_endpoints = db.query(Endpoint).filter(Endpoint.is_active == True).count()

    unresolved_security_ids = {
        row[0] for row in
        db.query(SecurityFinding.endpoint_id)
          .filter(SecurityFinding.resolved == False)
          .distinct()
          .all()
    }

    unresolved_leak_ids = {
        row[0] for row in
        db.query(DataLeakFinding.endpoint_id)
          .filter(DataLeakFinding.resolved == False)
          .distinct()
          .all()
    }

    unhealthy_ids = unresolved_security_ids | unresolved_leak_ids

    unhealthy_active_count = 0
    if unhealthy_ids:
        unhealthy_active_count = (
            db.query(Endpoint)
              .filter(Endpoint.is_active == True, Endpoint.id.in_(unhealthy_ids))
              .count()
        )

    healthy_endpoints = active_endpoints - unhealthy_active_count

    if active_endpoints > 0:
        health_score = round((healthy_endpoints / active_endpoints) * 100, 2)
    else:
        health_score = 100.0

    return {
        "total_endpoints": total_endpoints,
        "active_endpoints": active_endpoints,
        "healthy_endpoints": healthy_endpoints,
        "unhealthy_endpoints": unhealthy_active_count,
        "health_score_percentage": health_score,
    }


def get_traffic_trend(db: Session, range_days: int = 30) -> list[dict]:
    start_date = date.today() - timedelta(days=range_days)

    rows = (
        db.query(
            UsageDailySummary.usage_date,
            func.sum(UsageDailySummary.total_calls).label("total_calls")
        )
        .filter(UsageDailySummary.usage_date >= start_date)
        .group_by(UsageDailySummary.usage_date)
        .order_by(UsageDailySummary.usage_date.asc())
        .all()
    )

    return [{"usage_date": row.usage_date, "total_calls": row.total_calls or 0} for row in rows]


def get_health_distribution(db: Session) -> dict:
    # endpoint_ids with an unresolved HIGH severity security finding
    critical_from_security = {
        row[0] for row in
        db.query(SecurityFinding.endpoint_id)
          .filter(SecurityFinding.resolved == False, SecurityFinding.severity == SeverityEnum.high)
          .distinct()
          .all()
    }

    # endpoint_ids with ANY unresolved data leak (always critical)
    critical_from_leak = {
        row[0] for row in
        db.query(DataLeakFinding.endpoint_id)
          .filter(DataLeakFinding.resolved == False)
          .distinct()
          .all()
    }

    critical_ids = critical_from_security | critical_from_leak

    # endpoint_ids with an unresolved LOW or MEDIUM security finding (candidates for warning)
    low_medium_ids = {
        row[0] for row in
        db.query(SecurityFinding.endpoint_id)
          .filter(
              SecurityFinding.resolved == False,
              SecurityFinding.severity.in_([SeverityEnum.low, SeverityEnum.medium])
          )
          .distinct()
          .all()
    }

    # warning = has a low/medium finding, but is NOT already critical
    warning_ids = low_medium_ids - critical_ids

    total_endpoints = db.query(Endpoint).count()
    critical_count = len(critical_ids)
    warning_count = len(warning_ids)
    healthy_count = total_endpoints - critical_count - warning_count

    return {
        "healthy": healthy_count,
        "warning": warning_count,
        "critical": critical_count,
    }


def get_recent_alerts(db: Session, limit: int = 20) -> list[dict]:
    security_alerts = (
        db.query(SecurityFinding)
          .order_by(SecurityFinding.detected_at.desc())
          .limit(limit)
          .all()
    )

    leak_alerts = (
        db.query(DataLeakFinding)
          .order_by(DataLeakFinding.detected_at.desc())
          .limit(limit)
          .all()
    )

    combined = []

    for finding in security_alerts:
        combined.append({
            "alert_type": "security",
            "endpoint_id": finding.endpoint_id,
            "severity_or_type": finding.severity.value,
            "detected_at": finding.detected_at,
            "resolved": finding.resolved,
            "details": finding.details,
        })

    for leak in leak_alerts:
        combined.append({
            "alert_type": "data_leak",
            "endpoint_id": leak.endpoint_id,
            "severity_or_type": leak.leak_type.value,
            "detected_at": leak.detected_at,
            "resolved": leak.resolved,
            "details": leak.sample_snippet,
        })

    combined.sort(key=lambda x: x["detected_at"], reverse=True)

    return combined[:limit]