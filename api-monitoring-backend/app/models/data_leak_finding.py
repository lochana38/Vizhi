import enum
from sqlalchemy import Column, BigInteger, Boolean, Text, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class LeakTypeEnum(str, enum.Enum):
    pii_unmasked = "pii_unmasked"
    stack_trace_exposed = "stack_trace_exposed"
    sensitive_keyword = "sensitive_keyword"


class DataLeakFinding(Base):
    __tablename__ = "data_leak_findings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    endpoint_id = Column(BigInteger, ForeignKey("endpoints.id"), nullable=False)
    leak_type = Column(Enum(LeakTypeEnum), nullable=False)
    detected_at = Column(TIMESTAMP, server_default=func.now())
    sample_snippet = Column(Text, nullable=True)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(TIMESTAMP, nullable=True)

    endpoint = relationship("Endpoint")
