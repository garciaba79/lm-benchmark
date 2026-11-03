# Ministral 3 3B Instruct 2512
Model: ministral-3-3b-instruct-2512
Test: Code Fim 1
Created: 11/03/2026, 12:15:33 AM
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
    """
    Process a list of user event dictionaries and return a summary.
    """
    from datetime import datetime, timezone, timedelta

    if not events or not isinstance(user_id, str):
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

    total_events = len(events)
    event_counts = {}
    recent_events = []
    errors = []

    for event in events:
        try:
            timestamp_str = event["timestamp"]
            if not isinstance(timestamp_str, str):
                continue

            # Parse ISO 8601 timestamp
            event_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            event_time = event_time.replace(tzinfo=timezone.utc)

            # Check age and recent events
            if now - event_time <= max_age:
                recent_events.append(event)
            else:
                continue

            # Update event counts
            event_type = event.get("type", "")
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        except (KeyError, ValueError):
            errors.append(event.get("metadata", {}))

    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": len(recent_events),
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": max((e["timestamp"] for e in recent_events), default=None)
    }
```

230 t/s, 403 tokens, 2s
