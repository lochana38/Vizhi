from sqlalchemy.orm import Session
from app.models.duplicate_group import DuplicateGroup
from app.schemas.duplicate_group import DuplicateGroupCreate, DuplicateGroupUpdate


def create_duplicate_group(db: Session, data: DuplicateGroupCreate) -> DuplicateGroup:
    new_group = DuplicateGroup(**data.model_dump())
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


def get_duplicate_group(db: Session, group_id: int) -> DuplicateGroup | None:
    return db.query(DuplicateGroup).filter(DuplicateGroup.id == group_id).first()


def get_duplicate_groups(db: Session, skip: int = 0, limit: int = 100) -> list[DuplicateGroup]:
    return db.query(DuplicateGroup).offset(skip).limit(limit).all()


def update_duplicate_group(db: Session, group_id: int, data: DuplicateGroupUpdate) -> DuplicateGroup | None:
    group = get_duplicate_group(db, group_id)
    if group is None:
        return None
    for field, value in data.model_dump().items():
        setattr(group, field, value)
    db.commit()
    db.refresh(group)
    return group


def delete_duplicate_group(db: Session, group_id: int) -> DuplicateGroup | None:
    group = get_duplicate_group(db, group_id)
    if group is None:
        return None
    db.delete(group)
    db.commit()
    return group
