# API Monitoring Tool — Frontend (React + Vite)

## 1. Install dependencies

```bash
cd api-monitoring-frontend
npm install
```

## 2. Make sure your FastAPI backend is running

```bash
uvicorn app.main:app --reload
```
It should be reachable at http://127.0.0.1:8000 — check `src/api/client.js` if yours runs
somewhere else (e.g. a different port), and update `API_BASE_URL` there.

## 3. IMPORTANT: enable CORS on the backend

React (on localhost:5173) and FastAPI (on localhost:8000) are different origins as far as
the browser is concerned — without CORS enabled, every API call from React will be blocked
by the browser with a CORS error, even though the backend itself is working fine.

Add this to your `app/main.py`, right after `app = FastAPI(...)`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 4. Run the dev server

```bash
npm run dev
```
Opens at http://localhost:5173

## Pages / routes

| Route | What it shows |
|---|---|
| `/` | Overview — KPI cards, traffic trend, health distribution, recent alerts |
| `/security` | Security tab — filterable findings table, mark-resolved action |
| `/performance` | Performance tab — response-time trend, slowest endpoints, bandwidth |
| `/usage` | Usage tab — traffic ranking chart, unused endpoints, duplicate groups |
| `/import` | Upload an .xlsx file, shows shimmer while backend processes it |
| `/endpoints/:id` | Drilldown — usage graph, findings, duplicate membership for one endpoint |

## Structure

```
src/
  api/client.js       — single place with every backend call (axios)
  components/         — shared pieces: Layout (sidebar nav), KPICard, SeverityBadge,
                         EndpointPath (method+path renderer), Shimmer (loading skeletons)
  pages/               — one file per route, matches the tabs in the dashboard spec
  App.jsx              — routing table
  index.css            — Tailwind v4 import + shimmer animation
```

## Notes
- Charts use `recharts` (already familiar if you've used it in Claude artifacts before).
- Every page fetches its own data independently with `useEffect` + the functions from
  `api/client.js` — no global state library, kept intentionally simple.
- `EndpointPath` renders method+path in monospace with a color per HTTP verb — used
  consistently across every table so endpoints are always recognizable at a glance.
- This was built and verified with `npm run build` before packaging — it compiles cleanly.
