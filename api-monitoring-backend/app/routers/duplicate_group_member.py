from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.duplicate_group_member import (
    DuplicateGroupMemberCreate,
    DuplicateGroupMemberUpdate,
    DuplicateGroupMemberOut,
)
from app.crud import duplicate_group_member as crud_member

router = APIRouter(prefix="/duplicate-group-members", tags=["Duplicate Group Members"])


@router.post("/", response_model=DuplicateGroupMemberOut, status_code=status.HTTP_201_CREATED)
def create_member(data: DuplicateGroupMemberCreate, db: Session = Depends(get_db)):
    return crud_member.create_member(db, data)


@router.get("/", response_model=list[DuplicateGroupMemberOut])
def list_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_member.get_members(db, skip=skip, limit=limit)


@router.get("/by-group/{group_id}", response_model=list[DuplicateGroupMemberOut])
def list_members_for_group(group_id: int, db: Session = Depends(get_db)):
    return crud_member.get_members_by_group(db, group_id)


@router.get("/{member_id}", response_model=DuplicateGroupMemberOut)
def read_member(member_id: int, db: Session = Depends(get_db)):
    member = crud_member.get_member(db, member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Duplicate group member not found")
    return member


@router.put("/{member_id}", response_model=DuplicateGroupMemberOut)
def update_member(member_id: int, data: DuplicateGroupMemberUpdate, db: Session = Depends(get_db)):
    member = crud_member.update_member(db, member_id, data)
    if member is None:
        raise HTTPException(status_code=404, detail="Duplicate group member not found")
    return member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = crud_member.delete_member(db, member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Duplicate group member not found")
    return None
