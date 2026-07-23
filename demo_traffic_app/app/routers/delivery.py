"""
No database — delivery records live in memory only, same pattern as orders.py.
"""

import time
import random
from datetime import date, timedelta
from fastapi import APIRouter, HTTPException
from app.schemas.delivery import DeliveryCreateRequest, DeliveryResponse

router = APIRouter(prefix="/api/v1/delivery", tags=["Delivery"])

_deliveries: dict[int, dict] = {}
_next_id = 7000

STATUSES = ["pending", "dispatched", "in_transit", "delivered"]


@router.post("", response_model=DeliveryResponse)
def create_delivery(data: DeliveryCreateRequest):
    global _next_id
    time.sleep(random.uniform(0.05, 0.2))

    delivery_id = _next_id
    _next_id += 1

    record = {
        "delivery_id": delivery_id,
        "order_id": data.order_id,
        "status": "pending",
        "estimated_delivery_date": date.today() + timedelta(days=random.randint(2, 7)),
    }
    _deliveries[delivery_id] = record

    return DeliveryResponse(**record)


@router.get("/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(delivery_id: int):
    time.sleep(random.uniform(0.03, 0.1))

    record = _deliveries.get(delivery_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Delivery not found")

    # Randomly "progress" the status each time it's checked, just so repeated
    # polling looks like a real delivery moving through stages
    record["status"] = random.choice(STATUSES)

    return DeliveryResponse(**record)
