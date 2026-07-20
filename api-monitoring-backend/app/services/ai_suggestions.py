"""
Builds a compact summary of current dashboard state, sends it to Google's
free Gemini API, and asks for exactly 3 prioritized next actions.

Results are cached in memory for CACHE_TTL_SECONDS so rapid dashboard
reloads don't repeatedly hit the (rate-limited, even if free) LLM API.
This is a plain Python dict, not a database table or Redis — good enough
for a single-process demo. If you ever run multiple backend processes,
this cache would need to move somewhere shared (e.g. Redis) since each
process would otherwise keep its own separate cache.
"""

import os
import json
import time
import requests
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.crud import dashboard_overview as crud_overview
from app.crud import dashboard_security as crud_security
from app.crud import dashboard_performance as crud_performance
from app.crud import dashboard_usage as crud_usage

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

# Try the newest model first; if it's overloaded (503), fall back to an
# older, usually less contested model rather than failing the whole request.
MODEL_CANDIDATES = ["gemini-3.5-flash", "gemini-2.5-flash"]

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

# Which provider to actually use — switch by changing this one env var,
# nothing else in the file needs to change either way.
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")

CACHE_TTL_SECONDS = 600  # 10 minutes, as agreed

# Module-level dict = lives in memory as long as the server process is running.
_cache = {"data": None, "timestamp": 0}


def _build_summary(db: Session) -> dict:
    """Pull a SMALL, compact snapshot from data we already compute elsewhere —
    never send the whole database to the LLM, just the numbers that matter."""
    kpi = crud_overview.get_kpi_cards(db)
    security_summary = crud_security.get_security_summary(db)
    slowest = crud_performance.get_slowest_endpoints(db, limit=5)
    unused = crud_usage.get_unused_endpoints(db, days=30)

    return {
        "kpi_cards": kpi,
        "security_summary": security_summary,
        "top_5_slowest_endpoints": [
            {
                "path": row["endpoint"].path,
                "method": row["endpoint"].method.value,
                "avg_response_time_ms": row["avg_response_time_ms"],
            }
            for row in slowest
        ],
        "unused_endpoints_count": len(unused),
        "unused_endpoints_sample": [
            {"path": row["endpoint"].path, "method": row["endpoint"].method.value}
            for row in unused[:5]
        ],
    }


def _build_prompt(summary: dict) -> str:
    return f"""You are an API monitoring assistant. Based on this dashboard summary,
suggest exactly 3 prioritized next actions for the engineering team.

Dashboard summary (JSON):
{json.dumps(summary, indent=2, default=str)}

Respond with ONLY a JSON array of exactly 3 objects, no other text, no markdown fences.
Each object must have exactly these keys:
- "title": short action title (max 8 words)
- "description": 1-2 sentence explanation of why this matters, referencing the actual numbers above
- "priority": one of "high", "medium", "low"

Order the array from highest to lowest priority."""


def _call_gemini(prompt: str, max_retries_per_model: int = 2) -> list[dict]:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in your .env file.")

    last_error = None

    # Outer loop: try each model in order (newest first, then fall back)
    for model_name in MODEL_CANDIDATES:
        url = f"{GEMINI_BASE}/{model_name}:generateContent"

        # Inner loop: retry the SAME model a couple times before giving up on it
        for attempt in range(max_retries_per_model):
            try:
                response = requests.post(
                    url,
                    headers={
                        "x-goog-api-key": GEMINI_API_KEY,
                        "Content-Type": "application/json",
                    },
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"responseMimeType": "application/json"},
                    },
                    timeout=20,
                )

                if response.status_code == 503:
                    last_error = requests.exceptions.HTTPError(f"{model_name} overloaded (503)")
                    if attempt < max_retries_per_model - 1:
                        time.sleep(2 ** attempt)
                        continue
                    break  # give up on this model, fall through to the next candidate

                response.raise_for_status()

                data = response.json()
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                actions = json.loads(raw_text)

                if not isinstance(actions, list):
                    raise ValueError("Gemini did not return a JSON array as expected.")

                return actions  # success — stop trying further models

            except requests.exceptions.HTTPError as e:
                last_error = e
                break  # non-503 HTTP error — no point retrying the same model

    # Every model + retry attempt failed
    raise last_error


def _call_groq(prompt: str, max_retries: int = 2) -> list[dict]:
    """
    Groq uses the OpenAI-compatible chat completions format, which is
    structured differently from Gemini's — different request shape AND
    different place the actual text comes back in the response.
    """
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set in your .env file.")

    last_error = None
    for attempt in range(max_retries):
        try:
            response = requests.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"},
                },
                timeout=20,
            )
            response.raise_for_status()

            data = response.json()
            raw_text = data["choices"][0]["message"]["content"]
            parsed = json.loads(raw_text)

            # Groq's JSON mode requires a JSON OBJECT at the top level, not a bare
            # array like Gemini allowed — so we ask the prompt for {"actions": [...]}
            # when using Groq, and unwrap it here.
            actions = parsed["actions"] if isinstance(parsed, dict) else parsed

            if not isinstance(actions, list):
                raise ValueError("Groq did not return a JSON array as expected.")

            return actions

        except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue

    raise last_error


def _call_llm(prompt: str) -> list[dict]:
    """Single entry point — routes to whichever provider AI_PROVIDER selects."""
    if AI_PROVIDER == "groq":
        # Groq's JSON mode needs an object wrapper, not a bare array — see _call_groq
        groq_prompt = prompt + '\n\nWrap your answer as: {"actions": [ ...the 3 objects... ]}'
        return _call_groq(groq_prompt)
    return _call_gemini(prompt)

def get_next_actions(db: Session, force_refresh: bool = False) -> dict:
    now = time.time()
    cache_age = now - _cache["timestamp"]

    if not force_refresh and _cache["data"] is not None and cache_age < CACHE_TTL_SECONDS:
        return {
            "actions": _cache["data"],
            "generated_at": _cache["generated_at"],
            "cached": True,
            "provider": AI_PROVIDER,
        }

    summary = _build_summary(db)
    prompt = _build_prompt(summary)
    actions = _call_llm(prompt)

    generated_at = datetime.now(timezone.utc)
    _cache["data"] = actions
    _cache["timestamp"] = now
    _cache["generated_at"] = generated_at

    return {
        "actions": actions,
        "generated_at": generated_at,
        "cached": False,
        "provider": AI_PROVIDER,
    }
