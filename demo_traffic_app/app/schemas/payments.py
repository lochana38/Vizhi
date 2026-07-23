from pydantic import BaseModel


class PaymentTokenRequest(BaseModel):
    card_number: str
    expiry: str
    cvv: str


class PaymentTokenResponse(BaseModel):
    payment_token: str


class PaymentProcessRequest(BaseModel):
    order_id: int
    payment_token: str
    amount: float


class PaymentProcessResponse(BaseModel):
    payment_id: int
    status: str
    amount: float
