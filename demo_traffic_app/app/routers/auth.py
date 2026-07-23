"""
No database — a single hardcoded fake user, kept in memory, just so login
has something to check against. Purely for generating realistic traffic.
"""

import time
import random
from fastapi import APIRouter, HTTPException
from app.schemas.auth import LoginRequest, LoginResponse, LogoutResponse

router = APIRouter(prefix="/api/v1", tags=["Auth"])

FAKE_USER = {"username": "demo", "password": "demo123"}


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    time.sleep(random.uniform(0.05, 0.15))

    if data.username != FAKE_USER["username"] or data.password != FAKE_USER["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return LoginResponse(token="demo-token-123", expires_in_seconds=3600)


@router.post("/logout", response_model=LogoutResponse)
def logout():
    time.sleep(random.uniform(0.02, 0.08))
    return LogoutResponse(message="Logged out")
