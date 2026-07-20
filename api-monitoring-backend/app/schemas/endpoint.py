from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.endpoint import MethodEnum, SourceEnum, AuthTypeEnum


class EndpointBase(BaseModel):
    path: str
    method: MethodEnum
    name: Optional[str] = None
    description: Optional[str] = None
    source: SourceEnum
    expected_auth_type: AuthTypeEnum = AuthTypeEnum.none
    is_active: bool = True
    tags: Optional[List[str]] = None


class EndpointCreate(EndpointBase):
    pass


class EndpointUpdate(EndpointBase):
    pass


class EndpointOut(EndpointBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True