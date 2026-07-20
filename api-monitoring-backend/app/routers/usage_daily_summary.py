from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usage_daily_summary import (
    UsageDailySummaryCreate,
    UsageDailySummaryUpdate,
    UsageDailySummaryOut,
)
from app.crud import usage_daily_summary as crud_summary

router = APIRouter(prefix="/usage-daily-summary", tags=["Usage Daily Summary"])


@router.post("/", response_model=UsageDailySummaryOut, status_code=status.HTTP_201_CREATED)
def create_summary(data: UsageDailySummaryCreate, db: Session = Depends(get_db)):
    return crud_summary.create_summary(db, data)


@router.get("/", response_model=list[UsageDailySummaryOut])
def list_summaries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_summary.get_summaries(db, skip=skip, limit=limit)


@router.get("/by-endpoint/{endpoint_id}", response_model=list[UsageDailySummaryOut])
def list_summaries_for_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    return crud_summary.get_summaries_by_endpoint(db, endpoint_id)


@router.get("/{summary_id}", response_model=UsageDailySummaryOut)
def read_summary(summary_id: int, db: Session = Depends(get_db)):
    summary = crud_summary.get_summary(db, summary_id)
    if summary is None:
        raise HTTPException(status_code=404, detail="Usage summary not found")
    return summary


@router.put("/{summary_id}", response_model=UsageDailySummaryOut)
def update_summary(summary_id: int, data: UsageDailySummaryUpdate, db: Session = Depends(get_db)):
    summary = crud_summary.update_summary(db, summary_id, data)
    if summary is None:
        raise HTTPException(status_code=404, detail="Usage summary not found")
    return summary


@router.delete("/{summary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_summary(summary_id: int, db: Session = Depends(get_db)):
    summary = crud_summary.delete_summary(db, summary_id)
    if summary is None:
        raise HTTPException(status_code=404, detail="Usage summary not found")
    return None
