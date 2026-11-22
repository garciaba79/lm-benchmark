# Gemma 4 26B A4B QAT
Model: google/gemma-4-26b-a4b-qat
Test: Code Fim 1
Created: 11/22/2026, 03:00:34 AM
Exported from: LM Studio (via test script)
Context 16K

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
    
    summary = {
        "user_id": user_id,
        "total_events": 0,
        "recent_events": 0,
        "event_counts": {},
        "errors": [],
        "last_event_time": None
    }

    if not events:
        return summary

    now = datetime.now(timezone.utc)
    threshold_time = now - timedelta(hours=max_age_hours)
    
    valid_timestamps = []
    
    for event in events:
        # Filter by type for error collection
        event_type = event.get("type")
        if not event_type:
            continue

        # Update counts
        summary["total_events"] += 1
        summary["event_counts"][event_type] = summary["event_counts"].get(event_type, 0) + 1

        # Handle errors
        if event_type == "error":
            summary["errors"].append(event.get("metadata", {}))

        # Parse timestamp
        ts_str = event.get("timestamp")
        if ts_str:
            try:
                # Handles both 'Z' and '+HH:MM' formats via fromisoformat in Python 3.11+
                # or basic ISO strings in older versions
                dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                
                valid_timestamps.append(dt)
                
                if dt >= threshold_time:
                    summary["recent_events"] += 1
                    
            except ValueError:
                continue

    if valid_timestamps:
        last_dt = max(valid_timestamps)
        summary["last_event_time"] = last_dt.isoformat().replace("+00:00", "Z")

    return summary

56 t/s, 666 tokens, 12s, 6%
