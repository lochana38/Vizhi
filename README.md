# VizhiOps

**An API monitoring tool that tells you what to do next, not just what went wrong.**

VizhiOps looks at the endpoints your application exposes, the traffic they get, and the problems hiding inside them, and turns all of that into a dashboard three kinds of people can actually use: developers, quality teams, and executives. It automatically detects security issues and duplicate endpoints on import, and uses an LLM to suggest the three most important things to do next, so nobody has to dig through logs to figure out where to start.

Read the full story behind why this was built: *https://lochanaragupathy.com/blogs/the-bug-that-passed-staging-and-broke-production/*

---

## Architecture

### System Context

How VizhiOps sits between the application being monitored and the people who need to act on its health.

![System Context Diagram](docs/diagrams/VizhiOps_SystemContext.png)

### Functional Flow

The full loop, from an API call happening to a developer resolving it and the health score updating as a result.

![Functional Flow Diagram](docs/diagrams/VizhiOps_FunctionalFlow.png)

A more detailed architecture document, including the data flow diagram and full technology stack, is available in `docs/`.

---

## Features

- **Dashboard for three audiences** — KPI cards and health score for executives, filterable security findings for QA, prioritized next actions for developers.
- **Automatic detection on import** — checks every endpoint for missing authentication and sensitive data exposed in URLs, and groups near-duplicate endpoints.
- **AI-generated next actions** — reads a summary of current system state and returns exactly three ranked actions, powered by Gemini with Groq as a fallback provider.
- **Excel-based bulk import** — upload endpoints and usage data via a two-sheet workbook; no manual data entry per endpoint.
- **Endpoint drilldown** — full history, findings, and duplicate group membership for any single endpoint.
- **Demo traffic generator** — a separate, database-free FastAPI app (login, orders, payments, delivery) for generating realistic traffic to test the pipeline end to end.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS, Recharts, Axios |
| Backend | Python, FastAPI, Pydantic |
| Data Access | SQLAlchemy ORM |
| Database | MySQL |
| GenAI / LLM | Google Gemini (with Groq as an alternate provider) |
| Data Ingestion | Excel (.xlsx) via pandas + openpyxl |

---

## Project Structure

```
VizhiOps/
├── api-monitoring-backend/     # FastAPI backend
│   └── app/
│       ├── models/             # SQLAlchemy table definitions
│       ├── schemas/            # Pydantic request/response shapes
│       ├── crud/                # Database query functions
│       ├── routers/             # API endpoints
│       └── services/            # Detection rules, AI suggestion engine
├── api-monitoring-frontend/    # React dashboard
│   └── src/
│       ├── pages/                # Overview, Security, Performance, Usage, Import, Drilldown
│       ├── components/           # Shared UI (KPI cards, charts, badges)
│       └── api/                  # Backend API client
├── demo_traffic_app/           # Standalone traffic generator, no database
└── docs/                       # Architecture document and diagrams
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL 8

### 1. Database Setup

VizhiOps does not require any manual schema setup or migration tool. On first run, SQLAlchemy automatically creates every table from the backend's models, as long as the target database already exists (empty).

Create an empty database in MySQL:

```sql
CREATE DATABASE vizhi;
```

That's it. Once the backend starts (Step 2 below), all tables (`endpoints`, `security_findings`, `data_leak_findings`, `usage_daily_summary`, `duplicate_groups`, `duplicate_group_members`, `bulk_uploads`, `settings`) are created automatically to match the current models. No manual `CREATE TABLE` statements are needed.

### 2. Backend

```bash
cd api-monitoring-backend
python -m venv venv
venv\Scripts\Activate.ps1        # Windows
pip install -r requirements.txt
```

Create a `.env` file in `api-monitoring-backend/`:

```
DATABASE_URL=mysql+pymysql://DB_USER:DB_PASSWORD@DB_HOST:3306/DB_NAME
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
AI_PROVIDER=gemini
```

Run the server:

```bash
uvicorn app.main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`.

### 3. Frontend

```bash
cd api-monitoring-frontend
npm install
npm run dev
```

Runs at `http://localhost:5173`. Make sure CORS is enabled on the backend for this origin (see backend `main.py`).

### 4. Demo Traffic App (optional)

A separate, database-free app for generating realistic traffic to test the import pipeline.

```bash
cd demo_traffic_app
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --port 9000 --reload
```

---

## How Data Gets In

1. Export or generate endpoint and usage data as a two-sheet Excel file (`Endpoints` and `Usage`).
2. Upload it through the Import page.
3. VizhiOps parses the file, inserts the data, and automatically runs security and duplicate detection.
4. The dashboard and AI suggestion engine reflect the new data immediately.

---

## Roadmap

- **Phase 1 — Automated Capture**: remove the manual Excel export, push traffic into VizhiOps on a schedule.
- **Phase 2 — AI Agent (Anomaly & Leak Detection)**: inspect live request/response pairs directly, enabling data-leak detection and behavioral anomaly detection that a static Excel snapshot cannot support.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
