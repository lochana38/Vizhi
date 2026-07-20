from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.duplicate_group import DuplicateGroupCreate, DuplicateGroupUpdate, DuplicateGroupOut
from app.crud import duplicate_group as crud_group

router = APIRouter(prefix="/duplicate-groups", tags=["Duplicate Groups"])


@router.post("/", response_model=DuplicateGroupOut, status_code=status.HTTP_201_CREATED)
def create_group(data: DuplicateGroupCreate, db: Session = Depends(get_db)):
    return crud_group.create_duplicate_group(db, data)


@router.get("/", response_model=list[DuplicateGroupOut])
def list_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_group.get_duplicate_groups(db, skip=skip, limit=limit)


@router.get("/{group_id}", response_model=DuplicateGroupOut)
def read_group(group_id: int, db: Session = Depends(get_db)):
    group = crud_group.get_duplicate_group(db, group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Duplicate group not found")
    return group


@router.put("/{group_id}", response_model=DuplicateGroupOut)
def update_group(group_id: int, data: DuplicateGroupUpdate, db: Session = Depends(get_db)):
    group = crud_group.update_duplicate_group(db, group_id, data)
    if group is None:
        raise HTTPException(status_code=404, detail="Duplicate group not found")
    return group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = crud_group.delete_duplicate_group(db, group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Duplicate group not found")
    return None
