"""
No database — orders live in a plain in-memory dict for the lifetime of the
process. Restarting the server wipes them. That's fine, this app only exists
to generate traffic for the logging middleware to capture.
"""

import time
import random
from fastapi import APIRouter, HTTPException
from app.schemas.orders import OrderCreateRequest, OrderResponse

router = APIRouter(prefix="/api/v1", tags=["Orders"])

# In-memory "table" — just a dict keyed by order_id
_orders: dict[int, dict] = {}
_next_id = 1000


@router.post("/orders", response_model=OrderResponse)
def create_order(data: OrderCreateRequest):
    global _next_id
    time.sleep(random.uniform(0.1, 0.4))

    order_id = _next_id
    _next_id += 1

    total = sum(item.quantity * random.uniform(5, 50) for item in data.items)
    order = {
        "order_id": order_id,
        "status": "created",
        "total_amount": round(total, 2),
        "items": [item.model_dump() for item in data.items],
    }
    _orders[order_id] = order

    return OrderResponse(**order)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    time.sleep(random.uniform(0.03, 0.1))

    order = _orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return OrderResponse(**order)
