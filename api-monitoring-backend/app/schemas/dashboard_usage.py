from pydantic import BaseModel
from datetime import date
from typing import Optional
from decimal import Decimal
from app.schemas.endpoint import EndpointOut


class TrafficRankingOut(BaseModel):
    endpoint: EndpointOut
    total_calls: int


class UnusedEndpointOut(BaseModel):
    endpoint: EndpointOut
    last_called: Optional[date] = None


class DuplicateGroupMemberBriefOut(BaseModel):
    endpoint: EndpointOut
    similarity_score: Optional[Decimal] = None


class DuplicateGroupWithMembersOut(BaseModel):
    id: int
    group_label: Optional[str] = None
    members: list[DuplicateGroupMemberBriefOut]
