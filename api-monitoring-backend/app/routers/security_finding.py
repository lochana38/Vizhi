from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.security_finding import SecurityFindingCreate, SecurityFindingUpdate, SecurityFindingOut
from app.crud import security_finding as crud_finding

router = APIRouter(
    prefix="/security-findings",
    tags=["Security Findings"]
)


@router.post("/", response_model=SecurityFindingOut, status_code=status.HTTP_201_CREATED)
def create_finding(data: SecurityFindingCreate, db: Session = Depends(get_db)):
    return crud_finding.create_security_finding(db, data)


@router.get("/", response_model=list[SecurityFindingOut])
def list_findings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_finding.get_security_findings(db, skip=skip, limit=limit)


@router.get("/by-endpoint/{endpoint_id}", response_model=list[SecurityFindingOut])
def list_findings_for_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    return crud_finding.get_security_findings_by_endpoint(db, endpoint_id)


@router.get("/{finding_id}", response_model=SecurityFindingOut)
def read_finding(finding_id: int, db: Session = Depends(get_db)):
    finding = crud_finding.get_security_finding(db, finding_id)
    if finding is None:
        raise HTTPException(status_code=404, detail="Security finding not found")
    return finding


@router.put("/{finding_id}", response_model=SecurityFindingOut)
def update_finding(finding_id: int, data: SecurityFindingUpdate, db: Session = Depends(get_db)):
    finding = crud_finding.update_security_finding(db, finding_id, data)
    if finding is None:
        raise HTTPException(status_code=404, detail="Security finding not found")
    return finding


@router.delete("/{finding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_finding(finding_id: int, db: Session = Depends(get_db)):
    finding = crud_finding.delete_security_finding(db, finding_id)
    if finding is None:
        raise HTTPException(status_code=404, detail="Security finding not found")
    return None