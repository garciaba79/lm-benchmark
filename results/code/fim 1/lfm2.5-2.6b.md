# LFM2.5 2.6B
Model: lfm2.5-2.6b
Test: Code Fim 1
Created: 11/02/2026, 11:19:06 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Complete the following Python function. Only output the completed function (no explanations, no extra text, no markdown). Fill in the missing logic where indicated by the comments.

def process_user_events(events: list[dict], user_id: str, max_age_hours: int = 24) -> dict:
    """
    Process a list of user event dictionaries and return a summary.
    
    Each event dict has:
    - "timestamp": ISO 8601 string
    - "type": str (e.g. "login", "purchase", "view", "error")
    - "metadata": dict (optional extra fields)
    
    Return a dict with:
    - "user_id": the given user_id
    - "total_events": int
    - "recent_events": int (events within max_age_hours)
    - "event_counts": dict mapping event type -> count
    - "errors": list of error event metadata (or empty list)
    - "last_event_time": ISO string of the most recent event, or None
    """
    from datetime import datetime, timezone, timedelta
    
    # TODO: Implement the processing logic here
    # Filter events for the user, calculate age, aggregate counts,
    # collect errors, and determine the most recent timestamp.
    # Handle missing/invalid timestamps and empty input gracefully.
    
    pass  # Replace this with the full implementation

> #### 🤖 Assistant

def process_user_events(events: list[dict], user_id: str, max_age_hours: int = 24) -> dict:
    """
    Process a list of user event dictionaries and return a summary.
    
    Each event dict has:
    - "timestamp": ISO 8601 string
    - "type": str (e.g. "login", "purchase", "view", "error")
    - "metadata": dict (optional extra fields)
    
    Return a dict with:
    - "user_id": the given user_id
    - "total_events": int
    - "recent_events": int (events within max_age_hours)
    - "event_counts": dict mapping event type -> count
    - "errors": list of error event metadata (or empty list)
    - "last_event_time": ISO string of the most recent event, or None
    """
    from datetime import datetime, timedelta

    # Filter events for the specified user
    filtered = [e for e in events if isinstance(e.get("user_id"), str) and e["user_id"] == user_id]

    total_events = len(filtered)

    if not filtered:
        return {
            "user_id": user_id,
            "total_events": 0,
            "recent_events": 0,
            "event_counts": {},
            "errors": [],
            "last_event_time": None
        }

    # Determine the most recent timestamp among the filtered events
    try:
        max_ts = max(datetime.fromisoformat(e["timestamp"]) for e in filtered)
    except Exception:
        return {
            "user_id": user_id,
            "total_events": 0,
            "recent_events": 0,
            "event_counts": {},
            "errors": [],
            "last_event_time": None
        }

    # Define the time window we consider recent (max_age_hours from most recent event)
    max_age = max(0, max_age_hours)
    recent_window = timedelta(hours=max_age)

    recent_events = 0
    event_counts = {}
    error_meta = []

    for ev in filtered:
        # Parse timestamp; skip malformed entries
        try:
            ts = datetime.fromisoformat(ev["timestamp"])
        except Exception:
            continue

        if ts >= max_ts - recent_window:
            recent_events += 1

        typ = ev.get("type")
        if typ:
            event_counts[typ] = event_counts.get(typ, 0) + 1

        # Collect metadata from error events
        if typ == "error" and "metadata" in ev:
            error_meta.append(ev["metadata"])

    last_event_time = max_ts.isoformat()

    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": error_meta,
        "last_event_time": last_event_time
    }

253 t/s, 3390 tokens, 13s
