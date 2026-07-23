from pydantic import BaseModel
from datetime import date
from typing import Optional


class DeliveryCreateRequest(BaseModel):
    order_id: int
    address: str


class DeliveryResponse(BaseModel):
    delivery_id: int
    order_id: int
    status: str
    estimated_delivery_date: Optional[date] = None
