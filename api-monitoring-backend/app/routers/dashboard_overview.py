from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session


from app.database import get_db
from app.schemas.dashboard_overview import (
    KPICardsOut,
    TrafficTrendPointOut,
    HealthDistributionOut,
    RecentAlertOut,
)
from app.crud import dashboard_overview as crud_overview

router = APIRouter(prefix="/dashboard", tags=["Dashboard - Overview"])


@router.get("/kpi-cards", response_model=KPICardsOut)
def kpi_cards(db: Session = Depends(get_db)):
    return crud_overview.get_kpi_cards(db)


@router.get("/traffic-trend", response_model=list[TrafficTrendPointOut])
def traffic_trend(
    range: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    db: Session = Depends(get_db),
):
    return crud_overview.get_traffic_trend(db, range_days=range)


@router.get("/health-distribution", response_model=HealthDistributionOut)
def health_distribution(db: Session = Depends(get_db)):
    return crud_overview.get_health_distribution(db)


@router.get("/recent-alerts", response_model=list[RecentAlertOut])
def recent_alerts(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud_overview.get_recent_alerts(db, limit=limit)