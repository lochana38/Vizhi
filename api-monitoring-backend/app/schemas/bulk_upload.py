from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.bulk_upload import SourceTypeEnum, StatusEnum


class BulkUploadBase(BaseModel):
    filename: str
    filepath: str
    source_type: SourceTypeEnum
    total_records: int = 0
    successful_imports: int = 0
    failed_imports: int = 0
    skipped_imports: int = 0
    status: StatusEnum = StatusEnum.pending
    notes: Optional[str] = None


class BulkUploadCreate(BulkUploadBase):
    pass


class BulkUploadUpdate(BulkUploadBase):
    pass


class BulkUploadOut(BulkUploadBase):
    id: int
    imported_at: datetime

    class Config:
        from_attributes = True
