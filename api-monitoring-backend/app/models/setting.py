from sqlalchemy import Column, BigInteger, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class Setting(Base):
    __tablename__ = "settings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text, nullable=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
