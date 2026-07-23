from pydantic import BaseModel
from typing import Optional


class OrderItem(BaseModel):
    product_id: int
    quantity: int


class OrderCreateRequest(BaseModel):
    items: list[OrderItem]
    shipping_address: str


class OrderResponse(BaseModel):
    order_id: int
    status: str
    total_amount: float
    items: list[OrderItem]


class OrderNotFoundResponse(BaseModel):
    detail: str
