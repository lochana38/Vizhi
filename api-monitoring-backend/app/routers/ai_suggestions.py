from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ai_suggestions import AISuggestionsOut
from app.services import ai_suggestions as ai_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard - AI Suggestions"])


@router.get("/next-actions", response_model=AISuggestionsOut)
def next_actions(
    force_refresh: bool = Query(default=False, description="Bypass the 10-minute cache and call the LLM again"),
    db: Session = Depends(get_db),
):
    try:
        return ai_service.get_next_actions(db, force_refresh=force_refresh)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI suggestion service failed: {e}")
