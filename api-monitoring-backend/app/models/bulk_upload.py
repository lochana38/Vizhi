import enum
from sqlalchemy import Column, BigInteger, String, Integer, Text, TIMESTAMP, Enum
from sqlalchemy.sql import func
from app.database import Base


class SourceTypeEnum(str, enum.Enum):
    excel = "excel"
    postman = "postman"
    openapi = "openapi"
    swagger = "swagger"
    csv = "csv"
    json = "json"
    manual = "manual"
    other = "other"


class StatusEnum(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    completed_with_errors = "completed_with_errors"
    failed = "failed"


class BulkUpload(Base):
    __tablename__ = "bulk_uploads"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(1000), nullable=False)
    source_type = Column(Enum(SourceTypeEnum), nullable=False)
    total_records = Column(Integer, default=0)
    successful_imports = Column(Integer, default=0)
    failed_imports = Column(Integer, default=0)
    skipped_imports = Column(Integer, default=0)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.pending)
    notes = Column(Text, nullable=True)
    imported_at = Column(TIMESTAMP, server_default=func.now())
