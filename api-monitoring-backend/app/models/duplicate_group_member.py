from sqlalchemy import Column, BigInteger, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class DuplicateGroupMember(Base):
    __tablename__ = "duplicate_group_members"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    group_id = Column(BigInteger, ForeignKey("duplicate_groups.id"), nullable=False)
    endpoint_id = Column(BigInteger, ForeignKey("endpoints.id"), nullable=False)
    similarity_score = Column(Numeric(5, 2), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    endpoint = relationship("Endpoint")
    group = relationship("DuplicateGroup")
