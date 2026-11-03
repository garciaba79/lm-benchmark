# Qwen2.5 Coder 1.5B Instruct
Model: qwen2.5-coder-1.5b-instruct
Test: Code Fim 1
Created: 11/02/2026, 11:18:35 PM
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
from datetime import datetime, timezone, timedelta

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
    
    # Filter events for the user
    filtered_events = [event for event in events if event["user_id"] == user_id]
    
    # Calculate age of each event and filter within max_age_hours
    now = datetime.now(timezone.utc)
    recent_events = sum(1 for event in filtered_events if (now - datetime.fromisoformat(event["timestamp"])).total_seconds() / 3600 <= max_age_hours)
    
    # Aggregate counts of each event type
    event_counts = {}
    for event in filtered_events:
        if event["type"] in event_counts:
            event_counts[event["type"]] += 1
        else:
            event_counts[event["type"]] = 1
    
    # Collect errors and determine the most recent timestamp
    errors = [event for event in filtered_events if event["type"] == "error"]
    last_event_time = max(filtered_events, key=lambda x: datetime.fromisoformat(x["timestamp"]))["timestamp"] if events else None
    
    return {
        "user_id": user_id,
        "total_events": len(events),
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time
    }
```

297 t/s, 468 tokens, 2s
