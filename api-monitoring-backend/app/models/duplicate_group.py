from sqlalchemy import Column, BigInteger, String, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class DuplicateGroup(Base):
    __tablename__ = "duplicate_groups"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    group_label = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
