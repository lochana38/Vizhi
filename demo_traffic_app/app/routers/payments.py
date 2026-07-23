"""
No database, no real payment processing — everything here is fake and
in-memory. Deliberately slower than the other routers (real payment gateways
are usually the slowest hop in a request), useful for the Performance tab.
"""

import time
import random
from fastapi import APIRouter, HTTPException
from app.schemas.payments import (
    PaymentTokenRequest, PaymentTokenResponse,
    PaymentProcessRequest, PaymentProcessResponse,
)

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])

_next_payment_id = 5000


@router.post("/token", response_model=PaymentTokenResponse)
def get_payment_token(data: PaymentTokenRequest):
    time.sleep(random.uniform(0.1, 0.3))
    # NOTE: this route is intentionally a good example of a "sensitive data
    # in URL/body" pattern to later flag in the Security tab — it accepts a
    # raw card number in the request body, which a real system should never do.
    return PaymentTokenResponse(payment_token=f"tok_{random.randint(100000, 999999)}")


@router.post("/process", response_model=PaymentProcessResponse)
def process_payment(data: PaymentProcessRequest):
    global _next_payment_id
    time.sleep(random.uniform(0.4, 0.9))  # deliberately slow — payment gateways usually are

    if random.random() < 0.08:  # occasionally simulate a declined payment
        raise HTTPException(status_code=402, detail="Payment declined")

    payment_id = _next_payment_id
    _next_payment_id += 1

    return PaymentProcessResponse(payment_id=payment_id, status="completed", amount=data.amount)
