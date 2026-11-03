# Nemotron 3 Nano 4B
Model: nvidia/nemotron-3-nano-4b
Test: Code Fim 1
Created: 11/03/2026, 12:19:14 AM
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
    from datetime import datetime, timezone, timedelta

    if not events:
        return {
            "user_id": user_id,
            "total_events": 0,
            "recent_events": 0,
            "event_counts": {},
            "errors": [],
            "last_event_time": None
        }
    
    current_time = datetime.now(timezone.utc)
    cutoff_time = current_time - timedelta(hours=max_age_hours)

    total_events = 0
    recent_events = 0
    event_counts = {}
    errors = []
    last_event_time = None

    for event in events:
        if event.get("user_id") != user_id:
            continue
            
        timestamp_str = event.get("timestamp")
        if not timestamp_str or not isinstance(timestamp_str, str):
            errors.append(event)
            total_events += 1
            continue

        try:
            event_time = datetime.fromisoformat(timestamp_str).astimezone(timezone.utc)
        except (ValueError, TypeError):
            errors.append(event)
            total_events += 1
            continue

        if event.get("type") not in ("login", "purchase", "view", "error"):
            errors.append(event)
            total_events += 1
            continue

        is_recent = event_time >= cutoff_time
        if is_recent:
            recent_events += 1

        total_events += 1
        last_event_time = timestamp_str if last_event_time == None else max(timestamp_str, last_event_time)

        if event["type"] in event_counts:
            event_counts[event["type"]] += 1
        else:
            event_counts[event["type"]] = 1

    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time
    }

225 t/s, 609 tokens, 3s
