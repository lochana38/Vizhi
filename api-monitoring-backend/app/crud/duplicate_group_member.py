from sqlalchemy.orm import Session
from app.models.duplicate_group_member import DuplicateGroupMember
from app.schemas.duplicate_group_member import DuplicateGroupMemberCreate, DuplicateGroupMemberUpdate


def create_member(db: Session, data: DuplicateGroupMemberCreate) -> DuplicateGroupMember:
    new_member = DuplicateGroupMember(**data.model_dump())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


def get_member(db: Session, member_id: int) -> DuplicateGroupMember | None:
    return db.query(DuplicateGroupMember).filter(DuplicateGroupMember.id == member_id).first()


def get_members(db: Session, skip: int = 0, limit: int = 100) -> list[DuplicateGroupMember]:
    return db.query(DuplicateGroupMember).offset(skip).limit(limit).all()


def get_members_by_group(db: Session, group_id: int) -> list[DuplicateGroupMember]:
    return db.query(DuplicateGroupMember).filter(DuplicateGroupMember.group_id == group_id).all()


def update_member(db: Session, member_id: int, data: DuplicateGroupMemberUpdate) -> DuplicateGroupMember | None:
    member = get_member(db, member_id)
    if member is None:
        return None
    for field, value in data.model_dump().items():
        setattr(member, field, value)
    db.commit()
    db.refresh(member)
    return member


def delete_member(db: Session, member_id: int) -> DuplicateGroupMember | None:
    member = get_member(db, member_id)
    if member is None:
        return None
    db.delete(member)
    db.commit()
    return member
