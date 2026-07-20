import enum
from sqlalchemy import Column, BigInteger, String, Text, Boolean, JSON, TIMESTAMP, Enum
from sqlalchemy.sql import func
from app.database import Base


class MethodEnum(str, enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class SourceEnum(str, enum.Enum):
    excel_import = "excel_import"
    postman_import = "postman_import"
    discovered = "discovered"
    manual = "manual"
    log_entry = "log_entry"


class AuthTypeEnum(str, enum.Enum):
    none = "none"
    api_key = "api_key"
    bearer_token = "bearer_token"
    oauth = "oauth"
    basic = "basic"


class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    path = Column(String(500), nullable=False)
    method = Column(Enum(MethodEnum), nullable=False)
    name = Column(String(150), nullable=True)
    description = Column(Text, nullable=True)
    source = Column(Enum(SourceEnum), nullable=False)
    expected_auth_type = Column(Enum(AuthTypeEnum), nullable=False, default=AuthTypeEnum.none)
    is_active = Column(Boolean, default=True)
    tags = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())