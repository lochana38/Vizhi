"""
Handles the actual file upload + parsing, separate from bulk_upload.py
(which only does plain CRUD on the bulk_uploads table's metadata).

Expects an .xlsx file with exactly two sheets:

Sheet "Endpoints":
  path | method | name | description | expected_auth_type | is_active | tags

Sheet "Usage":
  endpoint_path | method | usage_date | total_calls | avg_response_time_ms |
  max_response_time_ms | error_count | total_bandwidth_bytes

Usage rows link back to an endpoint via (endpoint_path, method) matching,
since the real endpoint_id doesn't exist until that endpoint row is inserted
in this same request.
"""

import os
import shutil
import pandas as pd
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.bulk_upload import BulkUpload, SourceTypeEnum, StatusEnum
from app.models.endpoint import Endpoint, MethodEnum, SourceEnum, AuthTypeEnum
from app.models.usage_daily_summary import UsageDailySummary
from app.schemas.bulk_upload import BulkUploadOut
from app.services.detection import run_security_detection, run_duplicate_detection

router = APIRouter(prefix="/bulk-uploads", tags=["Bulk Upload Import"])

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/import", response_model=BulkUploadOut)
async def import_bulk_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported right now.")

    # Save the raw file to disk first — filepath gets stored on the bulk_uploads row
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    upload_row = BulkUpload(
        filename=file.filename,
        filepath=filepath,
        source_type=SourceTypeEnum.excel,
        status=StatusEnum.processing,
    )
    db.add(upload_row)
    db.commit()
    db.refresh(upload_row)

    try:
        endpoints_df = pd.read_excel(filepath, sheet_name="Endpoints")
        usage_df = pd.read_excel(filepath, sheet_name="Usage")
    except Exception as e:
        upload_row.status = StatusEnum.failed
        upload_row.notes = f"Could not read expected sheets 'Endpoints' and 'Usage': {e}"
        db.commit()
        db.refresh(upload_row)
        return upload_row

    successful = 0
    failed = 0
    skipped = 0
    notes: list[str] = []
    touched_endpoint_ids: set[int] = set()

    # ---- Step 1: Endpoints sheet ----
    path_method_to_id: dict[tuple[str, str], int] = {}

    for _, row in endpoints_df.iterrows():
        try:
            path = str(row["path"]).strip()
            method_str = str(row["method"]).strip().upper()

            existing = (
                db.query(Endpoint)
                .filter(Endpoint.path == path, Endpoint.method == MethodEnum(method_str))
                .first()
            )
            if existing:
                path_method_to_id[(path, method_str)] = existing.id
                touched_endpoint_ids.add(existing.id)
                skipped += 1
                continue

            new_endpoint = Endpoint(
                path=path,
                method=MethodEnum(method_str),
                name=_clean(row.get("name")),
                description=_clean(row.get("description")),
                source=SourceEnum.excel_import,
                expected_auth_type=AuthTypeEnum(_clean(row.get("expected_auth_type")) or "none"),
                is_active=bool(row.get("is_active")) if pd.notna(row.get("is_active")) else True,
                tags=_clean(row.get("tags")).split(",") if _clean(row.get("tags")) else None,
            )
            db.add(new_endpoint)
            db.commit()
            db.refresh(new_endpoint)

            path_method_to_id[(path, method_str)] = new_endpoint.id
            touched_endpoint_ids.add(new_endpoint.id)
            successful += 1

        except Exception as e:
            db.rollback()
            failed += 1
            notes.append(f"Endpoint row failed: {e}")

    # ---- Step 2: Usage sheet ----
    for _, row in usage_df.iterrows():
        try:
            path = str(row["endpoint_path"]).strip()
            method_str = str(row["method"]).strip().upper()
            endpoint_id = path_method_to_id.get((path, method_str))

            if endpoint_id is None:
                skipped += 1
                notes.append(f"Usage row skipped, no matching endpoint for {path} {method_str}")
                continue

            usage_row = UsageDailySummary(
                endpoint_id=endpoint_id,
                usage_date=pd.to_datetime(row["usage_date"]).date(),
                total_calls=int(row.get("total_calls") or 0),
                avg_response_time_ms=row.get("avg_response_time_ms") if pd.notna(row.get("avg_response_time_ms")) else None,
                max_response_time_ms=int(row["max_response_time_ms"]) if pd.notna(row.get("max_response_time_ms")) else None,
                error_count=int(row.get("error_count") or 0),
                total_bandwidth_bytes=int(row.get("total_bandwidth_bytes") or 0),
            )
            db.add(usage_row)
            db.commit()
            successful += 1

        except Exception as e:
            db.rollback()
            failed += 1
            notes.append(f"Usage row failed: {e}")

    # ---- Step 3: Auto-detection, only runs against endpoints touched in this import ----
    run_security_detection(db, touched_endpoint_ids)
    run_duplicate_detection(db, touched_endpoint_ids)

    # ---- Step 4: Finalize the bulk_uploads row ----
    upload_row.total_records = len(endpoints_df) + len(usage_df)
    upload_row.successful_imports = successful
    upload_row.failed_imports = failed
    upload_row.skipped_imports = skipped
    upload_row.status = StatusEnum.completed if failed == 0 else StatusEnum.completed_with_errors
    upload_row.notes = "; ".join(notes[:20]) if notes else None

    db.commit()
    db.refresh(upload_row)

    return upload_row


def _clean(value):
    """pandas gives NaN for empty Excel cells — convert that to a clean None/str."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    return str(value).strip()
