import enum
from sqlalchemy import Column, BigInteger, Boolean, Text, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship   


class IssueTypeEnum(str, enum.Enum):
    no_auth = "no_auth"
    no_https = "no_https"
    sensitive_data_in_url = "sensitive_data_in_url"


class SeverityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class SecurityFinding(Base):
    __tablename__ = "security_findings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    endpoint_id = Column(BigInteger, ForeignKey("endpoints.id"), nullable=False)
    issue_type = Column(Enum(IssueTypeEnum), nullable=False)
    severity = Column(Enum(SeverityEnum), nullable=False)
    detected_at = Column(TIMESTAMP, server_default=func.now())
    resolved = Column(Boolean, default=False)
    resolved_at = Column(TIMESTAMP, nullable=True)
    details = Column(Text, nullable=True)
    endpoint = relationship("Endpoint") 