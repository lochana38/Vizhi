from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import date, timedelta

from app.models.endpoint import Endpoint
from app.models.usage_daily_summary import UsageDailySummary
from app.models.duplicate_group import DuplicateGroup
from app.models.duplicate_group_member import DuplicateGroupMember


def get_traffic_ranking(db: Session, limit: int = 10, order: str = "desc") -> list[dict]:
    query = (
        db.query(
            Endpoint,
            func.sum(UsageDailySummary.total_calls).label("total_calls"),
        )
        .join(UsageDailySummary, UsageDailySummary.endpoint_id == Endpoint.id)
        .group_by(Endpoint.id)
    )

    total_calls_sum = func.sum(UsageDailySummary.total_calls)
    if order == "asc":
        query = query.order_by(total_calls_sum.asc())
    else:
        query = query.order_by(total_calls_sum.desc())

    rows = query.limit(limit).all()

    return [
        {"endpoint": row[0], "total_calls": int(row.total_calls or 0)}
        for row in rows
    ]


def get_unused_endpoints(db: Session, days: int = 30) -> list[dict]:
    cutoff = date.today() - timedelta(days=days)

    # Subquery: last date each endpoint actually had calls (total_calls > 0)
    last_call_subq = (
        db.query(
            UsageDailySummary.endpoint_id.label("endpoint_id"),
            func.max(UsageDailySummary.usage_date).label("last_called"),
        )
        .filter(UsageDailySummary.total_calls > 0)
        .group_by(UsageDailySummary.endpoint_id)
        .subquery()
    )

    # LEFT JOIN so endpoints with NO usage rows at all still show up (last_called = NULL)
    rows = (
        db.query(Endpoint, last_call_subq.c.last_called)
        .outerjoin(last_call_subq, last_call_subq.c.endpoint_id == Endpoint.id)
        .filter(
            (last_call_subq.c.last_called == None) | (last_call_subq.c.last_called < cutoff)
        )
        .all()
    )

    return [{"endpoint": row[0], "last_called": row[1]} for row in rows]


def get_duplicate_groups_with_members(db: Session) -> list[dict]:
    groups = db.query(DuplicateGroup).all()

    result = []
    for group in groups:
        members = (
            db.query(DuplicateGroupMember)
            .options(joinedload(DuplicateGroupMember.endpoint))
            .filter(DuplicateGroupMember.group_id == group.id)
            .all()
        )
        result.append({
            "id": group.id,
            "group_label": group.group_label,
            "members": [
                {"endpoint": m.endpoint, "similarity_score": m.similarity_score}
                for m in members
            ],
        })

    return result
