# Demo Traffic App — No database, in-memory only

Separate FastAPI app whose only purpose is to generate realistic API calls
(login, orders, payments, delivery) and log every request in memory. Feeds
into the Log Capture -> Excel page we built, which then feeds into your
main monitoring backend's bulk import.

## Structure

```
app/
  routers/
    auth.py       -> POST /api/v1/login, POST /api/v1/logout
    orders.py     -> POST /api/v1/orders, GET /api/v1/orders/{id}
    payments.py   -> POST /api/v1/payments/token, POST /api/v1/payments/process
    delivery.py   -> POST /api/v1/delivery, GET /api/v1/delivery/{id}
  schemas/
    auth.py, orders.py, payments.py, delivery.py  -> matching Pydantic models
main.py           -> wires routers together + the logging middleware
```

No models/, no crud/, no database.py — every "record" (orders, deliveries)
lives in a plain in-memory dict that resets when the server restarts. That's
intentional: this app exists only to generate traffic to capture, not to be
a real backend.

## Run it

```powershell
pip install -r requirements.txt
uvicorn main:app --port 9000 --reload
```

Runs on port 9000 (deliberately different from your main backend's 8000,
so you can run both at once).

## Try it manually first

Open http://127.0.0.1:9000/docs and call a few endpoints:
- POST /api/v1/login  {"username": "demo", "password": "demo123"}
- POST /api/v1/orders {"items": [{"product_id": 1, "quantity": 2}], "shipping_address": "123 Main St"}
- POST /api/v1/payments/token {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"}
- POST /api/v1/payments/process {"order_id": 1000, "payment_token": "tok_123456", "amount": 45.79}
- POST /api/v1/delivery {"order_id": 1000, "address": "123 Main St"}

Then check GET /logs — every call above should show up with its actual
response time, status code, and response size.

## Notes on what's deliberately built in

- /api/v1/login has NO auth required to call it (obviously — you're logging in)
  but /api/v1/payments/process simulates realistic slowness (0.4-0.9s), useful
  data for your Performance tab's "slowest endpoints" once imported.
- /api/v1/payments/token accepts a raw card number in the request body —
  flagged in the code comments as a deliberate "sensitive data" example for
  your Security tab's detection rules to eventually catch.
- Login fails ~10% of the time, payments decline ~8% of the time — gives your
  imported usage data a realistic error_count instead of always being zero.
- GET /api/v1/delivery/{id} randomly changes status each time you call it —
  call it a few times in a row to simulate a delivery progressing through
  stages, useful if you want varied traffic over "time" without waiting.

## Next step (tomorrow)
Run this alongside your main backend + React frontend, hit these demo
endpoints a bunch of times (curl loop, Postman runner, or just clicking
around in /docs), then use the Log Capture page to pull GET /logs and
download the aggregated Excel file — ready to feed into your real import.
