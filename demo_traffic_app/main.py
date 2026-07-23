"""
Standalone demo API — completely separate from your monitoring backend.
No database anywhere in this app. Its only job is to generate realistic
traffic (login, orders, payments, delivery) and record what happened to
each request, in plain memory.

GET /logs exposes everything recorded so far as JSON — the frontend fetches
this and converts it into an Excel file itself (see LogConverterPage.jsx).
"""

import time
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, orders, payments, delivery

app = FastAPI(title="Demo Traffic App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(delivery.router)

# Plain in-memory log — resets if the server restarts. That's fine for a demo;
# this app's only purpose is to exist long enough to generate some traffic.
request_logs: list[dict] = []


@app.middleware("http")
async def log_every_request(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000

    # Skip logging calls to /logs itself, so fetching the logs doesn't pollute the logs
    if request.url.path != "/logs":
        request_logs.append({
            "path": request.url.path,
            "method": request.method,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "response_time_ms": round(duration_ms, 2),
            "status_code": response.status_code,
            "response_size_bytes": int(response.headers.get("content-length", 0)),
        })

    return response


@app.get("/logs")
def get_logs():
    """Returns everything recorded so far. The frontend fetches this and
    builds the Excel file itself — this endpoint does no formatting at all."""
    return request_logs


@app.delete("/logs")
def clear_logs():
    """Handy for starting a fresh capture session without restarting the server."""
    request_logs.clear()
    return {"cleared": True}
