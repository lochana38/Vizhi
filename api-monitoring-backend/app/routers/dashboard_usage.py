from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Literal

from app.database import get_db
from app.schemas.dashboard_usage import (
    TrafficRankingOut,
    UnusedEndpointOut,
    DuplicateGroupWithMembersOut,
)
from app.crud import dashboard_usage as crud_usage

router = APIRouter(prefix="/usage", tags=["Dashboard - Usage"])

# separate router so the URL matches the PDF spec exactly: GET /duplicates (no /usage prefix)
duplicates_router = APIRouter(tags=["Dashboard - Usage"])


@router.get("/traffic-ranking", response_model=list[TrafficRankingOut])
def traffic_ranking(
    limit: int = Query(default=10, ge=1, le=100),
    order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db),
):
    return crud_usage.get_traffic_ranking(db, limit=limit, order=order)


@router.get("/unused-endpoints", response_model=list[UnusedEndpointOut])
def unused_endpoints(
    days: int = Query(default=30, ge=1, le=365, description="No calls within this many days counts as unused"),
    db: Session = Depends(get_db),
):
    return crud_usage.get_unused_endpoints(db, days=days)


@duplicates_router.get("/duplicates", response_model=list[DuplicateGroupWithMembersOut])
def duplicate_groups(db: Session = Depends(get_db)):
    return crud_usage.get_duplicate_groups_with_members(db)
