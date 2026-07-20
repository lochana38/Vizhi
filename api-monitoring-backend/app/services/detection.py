"""
Auto-detection rules, run right after a bulk import inserts endpoints.

Two things happen here:
1. Security finding detection — checks each endpoint against simple rules
   using only the data we actually have (no live traffic inspection).
2. Duplicate detection — groups endpoints whose paths are "the same shape"
   once numeric IDs are stripped out (e.g. /users/1 and /users/2 are the
   same underlying endpoint).
"""

import re
from sqlalchemy.orm import Session

from app.models.endpoint import Endpoint, AuthTypeEnum
from app.models.security_finding import SecurityFinding, IssueTypeEnum, SeverityEnum
from app.models.duplicate_group import DuplicateGroup
from app.models.duplicate_group_member import DuplicateGroupMember


SENSITIVE_KEYWORDS = ["password", "token", "ssn", "apikey", "api_key", "secret"]


def run_security_detection(db: Session, endpoint_ids: set[int]) -> None:
    """
    For every endpoint_id in the given set, check it against our rules and
    insert a SecurityFinding row if a rule matches and an unresolved finding
    of that same type doesn't already exist (avoids duplicate findings on
    repeated imports of the same endpoint).
    """
    for endpoint_id in endpoint_ids:
        endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
        if endpoint is None:
            continue

        # Rule 1: no authentication configured
        if endpoint.expected_auth_type == AuthTypeEnum.none:
            _create_finding_if_missing(
                db, endpoint_id, IssueTypeEnum.no_auth, SeverityEnum.high,
                "Endpoint has no authentication configured (auto-detected on import).",
            )

        # Rule 2: path contains a sensitive-looking keyword
        path_lower = endpoint.path.lower()
        if any(keyword in path_lower for keyword in SENSITIVE_KEYWORDS):
            _create_finding_if_missing(
                db, endpoint_id, IssueTypeEnum.sensitive_data_in_url, SeverityEnum.high,
                "Endpoint path may expose sensitive data directly in the URL (auto-detected on import).",
            )

    db.commit()


def _create_finding_if_missing(
    db: Session, endpoint_id: int, issue_type: IssueTypeEnum, severity: SeverityEnum, details: str
) -> None:
    already_exists = (
        db.query(SecurityFinding)
        .filter(
            SecurityFinding.endpoint_id == endpoint_id,
            SecurityFinding.issue_type == issue_type,
            SecurityFinding.resolved == False,
        )
        .first()
    )
    if already_exists:
        return

    db.add(SecurityFinding(
        endpoint_id=endpoint_id,
        issue_type=issue_type,
        severity=severity,
        details=details,
    ))


def _normalize_path(path: str) -> str:
    """
    Turns /users/123 and /users/456 into the same shape: /users/{id}
    Only strips purely numeric path segments — good enough for a demo,
    not a full path-templating engine.
    """
    return re.sub(r"/\d+", "/{id}", path)


def run_duplicate_detection(db: Session, touched_endpoint_ids: set[int]) -> None:
    """
    Compares EVERY endpoint in the table (not just the newly imported ones),
    because a new upload might introduce a duplicate of something imported
    weeks ago. Groups endpoints that share the same normalized path + method.
    """
    all_endpoints = db.query(Endpoint).all()

    groups_by_shape: dict[tuple[str, str], list[Endpoint]] = {}
    for ep in all_endpoints:
        key = (_normalize_path(ep.path), ep.method.value)
        groups_by_shape.setdefault(key, []).append(ep)

    for (shape, method), endpoints_in_group in groups_by_shape.items():
        if len(endpoints_in_group) < 2:
            continue  # no duplicates, nothing to do

        # Which of these endpoints are already grouped from a previous import?
        already_grouped_ids = {
            row.endpoint_id for row in
            db.query(DuplicateGroupMember)
              .filter(DuplicateGroupMember.endpoint_id.in_([e.id for e in endpoints_in_group]))
              .all()
        }

        ungrouped = [e for e in endpoints_in_group if e.id not in already_grouped_ids]
        if not ungrouped:
            continue  # this whole group was already recorded before

        # Reuse an existing group if one already covers this shape, else create one
        existing_member = (
            db.query(DuplicateGroupMember)
            .filter(DuplicateGroupMember.endpoint_id.in_(
                [e.id for e in endpoints_in_group if e.id in already_grouped_ids]
            ))
            .first()
        )

        if existing_member:
            group_id = existing_member.group_id
        else:
            new_group = DuplicateGroup(group_label=f"Similar paths: {shape} ({method})")
            db.add(new_group)
            db.commit()
            db.refresh(new_group)
            group_id = new_group.id

        for ep in ungrouped:
            db.add(DuplicateGroupMember(
                group_id=group_id,
                endpoint_id=ep.id,
                similarity_score=100.00,  # exact shape match; a fuzzier score could vary this later
            ))

    db.commit()
