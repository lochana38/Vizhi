from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.dashboard_drilldown import EndpointDrilldownOut, EndpointUsagePointOut
from app.crud import dashboard_drilldown as crud_drilldown

router = APIRouter(tags=["Dashboard - Drilldown"])


@router.get("/endpoints/{endpoint_id}/drilldown", response_model=EndpointDrilldownOut)
def endpoint_drilldown(
    endpoint_id: int,
    range: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    detail = crud_drilldown.get_endpoint_full_detail(db, endpoint_id, range_days=range)
    if detail is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return detail


@router.get("/usage/logs", response_model=list[EndpointUsagePointOut])
def usage_logs(
    endpoint_id: int,
    range: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    return crud_drilldown.get_endpoint_usage_timeseries(db, endpoint_id, range_days=range)
