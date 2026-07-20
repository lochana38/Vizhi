from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.data_leak_finding import DataLeakFindingCreate, DataLeakFindingUpdate, DataLeakFindingOut
from app.crud import data_leak_finding as crud_leak

router = APIRouter(prefix="/data-leak-findings", tags=["Data Leak Findings"])


@router.post("/", response_model=DataLeakFindingOut, status_code=status.HTTP_201_CREATED)
def create_finding(data: DataLeakFindingCreate, db: Session = Depends(get_db)):
    return crud_leak.create_data_leak_finding(db, data)


@router.get("/", response_model=list[DataLeakFindingOut])
def list_findings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_leak.get_data_leak_findings(db, skip=skip, limit=limit)


@router.get("/by-endpoint/{endpoint_id}", response_model=list[DataLeakFindingOut])
def list_findings_for_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    return crud_leak.get_data_leak_findings_by_endpoint(db, endpoint_id)


@router.get("/{finding_id}", response_model=DataLeakFindingOut)
def read_finding(finding_id: int, db: Session = Depends(get_db)):
    finding = crud_leak.get_data_leak_finding(db, finding_id)
    if finding is None:
        raise HTTPException(status_code=404, detail="Data leak finding not found")
    return finding


@router.put("/{finding_id}", response_model=DataLeakFindingOut)
def update_finding(finding_id: int, data: DataLeakFindingUpdate, db: Session = Depends(get_db)):
    finding = crud_leak.update_data_leak_finding(db, finding_id, data)
    if finding is None:
        raise HTTPException(status_code=404, detail="Data leak finding not found")
    return finding


@router.delete("/{finding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_finding(finding_id: int, db: Session = Depends(get_db)):
    finding = crud_leak.delete_data_leak_finding(db, finding_id)
    if finding is None:
        raise HTTPException(status_code=404, detail="Data leak finding not found")
    return None
