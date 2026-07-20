from sqlalchemy import Column, BigInteger, Integer, Numeric, Date, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class UsageDailySummary(Base):
    __tablename__ = "usage_daily_summary"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    endpoint_id = Column(BigInteger, ForeignKey("endpoints.id"), nullable=False)
    usage_date = Column(Date, nullable=False)
    total_calls = Column(BigInteger, default=0)
    avg_response_time_ms = Column(Numeric(10, 2), nullable=True)
    max_response_time_ms = Column(Integer, nullable=True)
    error_count = Column(BigInteger, default=0)
    total_bandwidth_bytes = Column(BigInteger, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    endpoint = relationship("Endpoint")
