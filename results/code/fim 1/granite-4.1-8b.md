# Granite 4.1 8B
Model: granite-4.1-8b
Test: Code Fim 1
Created: 11/03/2026, 12:39:30 AM
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
    """ Process a list of user event dictionaries and return a summary.
    
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

    user_events = [e for e in events if e.get("user_id") == user_id]
    
    total_events = len(user_events)

    now = datetime.now(timezone.utc)
    max_age_timedelta = timedelta(hours=max_age_hours)
    recent_cutoff = now - max_age_timedelta

    recent_events_count = 0
    event_counts = {}
    errors = []
    last_event_time = None
    
    for ev in user_events:
        try:
            ts = datetime.fromisoformat(ev["timestamp"].replace("Z", "+00:00"))
        except (ValueError, TypeError):
            # Skip events with invalid or missing timestamps
            continue

        if ts > recent_cutoff:
            recent_events_count += 1

        ev_type = ev.get("type")
        if ev_type in event_counts:
            event_counts[ev_type] += 1
        else:
            event_counts[ev_type] = 1

        last_event_time = max(last_event_time, ts) if last_event_time else ts

        if ev.get("type") == "error":
            errors.append(ev.get("metadata", {}))

    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events_count,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time.isoformat() if last_event_time else None
    }

124 t/s, 488 tokens, 4s
