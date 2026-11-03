# Gemma 4 12B
Model: google/gemma-4-12b
Test: Code Fim 1
Created: 11/03/2026, 12:56:15 AM
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
    - "type": str (e.g., "login", "purchase", "view", "error")
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

    now = datetime.now(timezone.utc)
    user_events = [e for e in events if e.get("user_id") == user_id]
    
    event_counts = {}
    errors = []
    recent_count = 0
    latest_ts = None

    for event in user_events:
        e_type = event.get("type")
        if e_type:
            event_counts[e_type] = event_counts.get(e_type, 0) + 1
        
        if e_type == "error":
            errors.append(event.get("metadata", {}))

        ts_str = event.get("timestamp")
        if ts_str:
            try:
                dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                
                if (now - dt) <= timedelta(hours=max_age_hours):
                    recent_count += 1
                
                if latest_ts is None or dt > latest_ts:
                    latest_ts = dt
            except (ValueError, TypeError):
                pass

    return {
        "user_id": user_id,
        "total_events": len(user_events),
        "recent_events": recent_count,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": latest_ts.isoformat() if latest_ts else None
    }

81 t/s, 589 tokens, 7s
