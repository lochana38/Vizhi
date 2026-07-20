from pydantic import BaseModel
from datetime import datetime


class ActionItemOut(BaseModel):
    title: str
    description: str
    priority: str  # "high" | "medium" | "low" — the LLM assigns this, not a DB enum


class AISuggestionsOut(BaseModel):
    actions: list[ActionItemOut]
    generated_at: datetime
    cached: bool
    provider: str  # "gemini" or "groq" — whichever actually answered this request
