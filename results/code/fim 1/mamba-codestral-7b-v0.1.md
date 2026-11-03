# Mamba Codestral 7B v0.1
Model: mamba-codestral-7b-v0.1
Test: Code Fim 1
Created: 11/03/2026, 12:29:26 AM
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

    event_counts = {}
    errors = []
    last_event_time = None
    total_events = 0
    recent_events = 0

    for event in events:
        if "timestamp" not in event or "type" not in event:
            continue

        try:
            timestamp = datetime.fromisoformat(event["timestamp"])
            age = (datetime.now(timezone.utc) - timestamp).total_seconds() / 3600

            if age > max_age_hours:
                continue

            event_type = event["type"]
            total_events += 1
            recent_events += 1 if age <= max_age_hours else 0
            last_event_time = timestamp.isoformat() if not last_event_time or timestamp > datetime.fromisoformat(last_event_time) else last_event_time

            event_counts[event_type] = event_counts.get(event_type, 0) + 1

            if "metadata" in event and event["type"] == "error":
                errors.append(event["metadata"])
        except ValueError:
            continue

    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time
    }

148 t/s, 403 tokens, 3s
