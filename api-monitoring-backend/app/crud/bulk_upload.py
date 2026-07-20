from sqlalchemy.orm import Session
from app.models.bulk_upload import BulkUpload
from app.schemas.bulk_upload import BulkUploadCreate, BulkUploadUpdate


def create_bulk_upload(db: Session, data: BulkUploadCreate) -> BulkUpload:
    new_upload = BulkUpload(**data.model_dump())
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)
    return new_upload


def get_bulk_upload(db: Session, upload_id: int) -> BulkUpload | None:
    return db.query(BulkUpload).filter(BulkUpload.id == upload_id).first()


def get_bulk_uploads(db: Session, skip: int = 0, limit: int = 100) -> list[BulkUpload]:
    return db.query(BulkUpload).offset(skip).limit(limit).all()


def update_bulk_upload(db: Session, upload_id: int, data: BulkUploadUpdate) -> BulkUpload | None:
    upload = get_bulk_upload(db, upload_id)
    if upload is None:
        return None
    for field, value in data.model_dump().items():
        setattr(upload, field, value)
    db.commit()
    db.refresh(upload)
    return upload


def delete_bulk_upload(db: Session, upload_id: int) -> BulkUpload | None:
    upload = get_bulk_upload(db, upload_id)
    if upload is None:
        return None
    db.delete(upload)
    db.commit()
    return upload
