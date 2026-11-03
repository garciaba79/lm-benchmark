# Ministral 3 8B Instruct 2512
Model: ministral-3-8b-instruct-2512
Test: Code Fim 1
Created: 11/03/2026, 12:42:21 AM
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

```python
def process_user_events(events: list[dict], user_id: str, max_age_hours: int = 24) -> dict:
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

    now = datetime.now(timezone.utc)
    max_age = timedelta(hours=max_age_hours)
    threshold = now - max_age

    total_count = 0
    recent_count = 0
    event_type_counts = {}
    error_metadata = []
    latest_time = None

    for event in events:
        try:
            timestamp_str = event.get("timestamp")
            if not timestamp_str:
                continue

            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)

            total_count += 1
            event_type = event.get("type", "")
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1

            if timestamp >= threshold:
                recent_count += 1

            if latest_time is None or timestamp > latest_time:
                latest_time = timestamp

            if event.get("type") == "error":
                error_metadata.append(event.get("metadata", {}))

        except (ValueError, AttributeError):
            continue

    return {
        "user_id": user_id,
        "total_events": total_count,
        "recent_events": recent_count,
        "event_counts": event_type_counts,
        "errors": error_metadata,
        "last_event_time": latest_time.isoformat() if latest_time else None
    }
```

124 t/s, 404 tokens, 3s
