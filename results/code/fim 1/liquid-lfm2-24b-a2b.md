# Lfm2 24B A2B
Model: liquid/lfm2-24b-a2b
Test: Code Fim 1
Created: 11/03/2026, 01:20:46 AM
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

    filtered_events = []
    event_counts = {}
    errors = []
    last_event_time = None

    for event in events:
        if event.get("type") != "login" and event.get("type") != "purchase" and event.get("type") != "view" and event.get("type") != "error":
            continue
        
        try:
            timestamp_str = event["timestamp"]
            timestamp = datetime.fromisoformat(timestamp_str).replace(tzinfo=timezone.utc)
        except (KeyError, ValueError):
            continue

        age = (datetime.now(timezone.utc) - timestamp).total_seconds() / 3600
        if age <= max_age_hours:
            filtered_events.append(event)

        event_type = event["type"]
        event_counts[event_type] = event_counts.get(event_type, 0) + 1

        if event_type == "error":
            errors.append(event.get("metadata", {}))
        
        if last_event_time is None or (timestamp - last_event_time).total_seconds() > 0:
            last_event_time = timestamp

    return {
        "user_id": user_id,
        "total_events": len(filtered_events),
        "recent_events": len(filtered_events),
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time.isoformat() if last_event_time else None
    }

146 t/s, 368 tokens, 3s
