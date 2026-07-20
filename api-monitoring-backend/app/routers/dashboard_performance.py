from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.dashboard_performance import (
    ResponseTimeTrendPointOut,
    SlowEndpointOut,
    BandwidthUsageOut,
)
from app.crud import dashboard_performance as crud_perf

router = APIRouter(prefix="/performance", tags=["Dashboard - Performance"])


@router.get("/response-time-trend", response_model=list[ResponseTimeTrendPointOut])
def response_time_trend(
    range: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    return crud_perf.get_response_time_trend(db, range_days=range)


@router.get("/slowest-endpoints", response_model=list[SlowEndpointOut])
def slowest_endpoints(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud_perf.get_slowest_endpoints(db, limit=limit)


@router.get("/bandwidth-usage", response_model=list[BandwidthUsageOut])
def bandwidth_usage(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud_perf.get_bandwidth_usage(db, limit=limit)
