from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.bulk_upload import BulkUploadCreate, BulkUploadUpdate, BulkUploadOut
from app.crud import bulk_upload as crud_upload

router = APIRouter(prefix="/bulk-uploads", tags=["Bulk Uploads"])


@router.post("/", response_model=BulkUploadOut, status_code=status.HTTP_201_CREATED)
def create_upload(data: BulkUploadCreate, db: Session = Depends(get_db)):
    return crud_upload.create_bulk_upload(db, data)


@router.get("/", response_model=list[BulkUploadOut])
def list_uploads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_upload.get_bulk_uploads(db, skip=skip, limit=limit)


@router.get("/{upload_id}", response_model=BulkUploadOut)
def read_upload(upload_id: int, db: Session = Depends(get_db)):
    upload = crud_upload.get_bulk_upload(db, upload_id)
    if upload is None:
        raise HTTPException(status_code=404, detail="Bulk upload not found")
    return upload


@router.put("/{upload_id}", response_model=BulkUploadOut)
def update_upload(upload_id: int, data: BulkUploadUpdate, db: Session = Depends(get_db)):
    upload = crud_upload.update_bulk_upload(db, upload_id, data)
    if upload is None:
        raise HTTPException(status_code=404, detail="Bulk upload not found")
    return upload


@router.delete("/{upload_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_upload(upload_id: int, db: Session = Depends(get_db)):
    upload = crud_upload.delete_bulk_upload(db, upload_id)
    if upload is None:
        raise HTTPException(status_code=404, detail="Bulk upload not found")
    return None
