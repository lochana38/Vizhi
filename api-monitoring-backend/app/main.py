from fastapi import FastAPI
from app.database import Base, engine
from app.routers import endpoint
from app.routers import security_finding
from app.routers import bulk_upload
from app.routers import data_leak_finding
from app.routers import duplicate_group_member
from app.routers import duplicate_group
from app.routers import setting
from app.routers import usage_daily_summary
from app.routers import dashboard_overview
from app.routers import dashboard_security
from app.routers import dashboard_usage
from app.routers import dashboard_drilldown
from app.routers import dashboard_performance
from app.routers import bulk_upload_import
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ai_suggestions





Base.metadata.create_all(bind=engine)  # creates any tables that don't exist yet (safe if they already do)

app = FastAPI(title="API Monitoring Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(endpoint.router)
app.include_router(security_finding.router)
app.include_router(bulk_upload.router)
app.include_router(data_leak_finding.router)
app.include_router(duplicate_group.router)
app.include_router(duplicate_group_member.router)
app.include_router(setting.router)
app.include_router(usage_daily_summary.router)
app.include_router(dashboard_overview.router)
app.include_router(dashboard_security.router)
app.include_router(dashboard_usage.router)
app.include_router(dashboard_performance.router)
app.include_router(dashboard_drilldown.router)
app.include_router(bulk_upload_import.router)
app.include_router(ai_suggestions.router)