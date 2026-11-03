# LFM2.5 1.2B Instruct
Model: lfm2.5-1.2b-instruct
Test: Code Fim 1
Created: 11/02/2026, 11:17:08 PM
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
    from datetime import datetime, timezone, timedelta

    total_events = len(events)
    recent_events_count = 0
    event_counts = {}
    errors = []
    last_event_time = None

    for event in events:
        user_match = event.get("metadata", {}).get(user_id) == user_id
        if not user_match:
            continue

        timestamp_str = event["timestamp"]
        try:
            event_time = datetime.fromisoformat(timestamp_str)
            age_hours = (event_time - timezone.utcnow()).total_seconds() / 3600
        except Exception:
            continue

        if age_hours <= max_age_hours and not errors and "error" in event.get("type", ""):
            errors.append(event["metadata"])
            last_event_time = event_time

    if recent_events_count == 0:
        return {"total_events": total_events, "recent_events": 0, "event_counts": {}, "errors": [], "last_event_time": None}

    filtered_events = [e for e in events if e.get("user_id") == user_id and 
                      (datetime.fromisoformat(e["timestamp"]) - last_event_time).total_seconds() < timedelta(hours=max_age_hours)]

    recent_count = len(filtered_events)
    event_counts = {}
    for event in filtered_events:
        event_type = event.get("type")
        if event_type in event_counts:
            event_counts[event_type] += 1
        else:
            event_counts[event_type] = 1

    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_count,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time
    }

529 t/s, 450 tokens, 1s
