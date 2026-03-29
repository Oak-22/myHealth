# ========================
# Event Aggregation
# ========================
# You are given a list of event records with the schema below
# Task: Write a function that returns a summary per user:

"""
Schema:
{
  user_id: {
      count: int,
      total_duration: int
  }
}

Rules:
- Only count records where duration is a positive integer
- Ignore records missing user_id or duration
- Do not mutate input
- No external libraries
"""

# Expected output for test input:
#{
#    "u1": {"count": 2, "total_duration": 30},
#    "u2": {"count": 1, "total_duration": 30}
#}




records: list[dict[str, object]] = [
    {"user_id": "u1", "event": "click", "duration": 10},
    {"user_id": "u1", "event": "scroll", "duration": 20},
    {"user_id": "u2", "event": "click", "duration": 30},
    {"user_id": "u1", "event": "hover", "duration": -5},   # invalid (negative)
    {"user_id": None, "event": "click", "duration": 15},   # invalid (missing user)
    {"user_id": "u2", "event": "scroll", "duration": 0},   # invalid (zero)
]

# ------------------------------------------------

from typing import Any, TypedDict
from collections.abc import Mapping

# dict[str, object] -> keys are strings, values can be anything
# Mapping[str, Any] -> I only assume a key-value interface
# TypedDict -> these specific keys exist and have specific value types

"""
In interview: 

    "Before I add defensive guards, I want to clarify the data contract. Is this function expected to receive validated,
    well-formed input, or is it operating at a boundary where malformed or heterogeneous records are possible?"

    "Heterogenous records are possible".

    "I define a TypedDict that represents the expected record shape, and then type-hint values as that shape, e.g. record: EventRecord"
    
"""


class EventRecord(TypedDict):
    # Create a class for TypedDict to clean/normalize loosely shaped data
    # No instantiation, no consturctor, no inhereitance tree. Just shape
    user_id: str
    event: str
    duration: int




def normalize_records_staging(raw: Any) -> list[EventRecord]:
    """
    Boundary/normalization layer (messy input allowed).
    Uses type 'Any' or 'Object' for the raw input and returns a clean list of normalized records.
    """
    # Defensive: raw might not be a list at all
    if not isinstance(raw, list):
        print(f"Raw record is of expected type list, got {type(raw).__name__}")
        #Fail-soft. Program still runs/executes if raw isn't a list. Observable.
        return []

    normalized: list[EventRecord] = []

    for item in raw:
        # Defensive: each item might not be dict-like
        if not isinstance(item, Mapping):
            continue

        # Pull fields (could be missing / wrong types)
        user_id = item.get("user_id")
        event = item.get("event")
        duration = item.get("duration")

        # Validate user_id: must be a non-empty string
        if not isinstance(user_id, str) or not user_id.strip():
            continue  # skip this record and move to the next iteration

        # Validate event_id:
        if not isinstance(event, str) or not event.strip():
            continue

        # Validate duration:
        if not isinstance(duration, int):
            continue
        if isinstance(duration, bool) or duration <= 0:
            continue

        # Now we can safely assert the normalized shape
        normalized.append(
            {
                "user_id": user_id,
                "event": event,
                "duration": duration
            }
        )

    return normalized



# Refactored summarizer: core logic assumes input is normalized by normalize_records_staging()
def event_records_summary_prod(records: list[EventRecord]) -> dict[str, dict[str, int]]:
    """
    Core summarizer. Assumes `records` are already normalized to `EventRecord` shape.

    Precondition: each `r` in `records` is a dict with keys `user_id` (non-empty str) and `duration` (positive int).
    No runtime validation is performed here to avoid duplicating boundary logic.
    """
    out: dict[str, dict[str, int]] = {}

    for r in records:
        user_id = r["user_id"]
        duration = r["duration"]

        if user_id not in out:
            out[user_id] = {"count": 0, "total_duration": 0}

        out[user_id]["count"] += 1
        out[user_id]["total_duration"] += duration

    return out



# Basic self-check (expected output for the sample 'records')
# Use the normalizer at the boundary, then call the core summarizer.
normalized = normalize_records_staging(records)
result = event_records_summary_prod(normalized)
print(result)

expected = {"u1": {"count": 2, "total_duration": 30}, "u2": {"count": 1, "total_duration": 30}}

assert result == expected, f"Unexpected result: {result} != {expected}"
print("Test passed: aggregation matches expected output")
