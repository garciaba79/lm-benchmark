# Phi 4
Model: microsoft/phi-4
Test: Code Fim 1
Created: 11/03/2026, 01:14:37 AM
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
    
    now = datetime.now(timezone.utc)
    event_counts = {}
    errors = []
    recent_count = 0
    total_count = 0
    last_event_time = None

    for event in events:
        if event.get("user_id") != user_id:
            continue
        
        try:
            timestamp = datetime.fromisoformat(event["timestamp"])
            if "Z" in event["timestamp"]:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
        except (KeyError, ValueError):
            timestamp = None

        total_count += 1
        event_type = event.get("type")

        if event_type:
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        if event_type == "error":
            errors.append(event.get("metadata", {}))
        
        if timestamp and last_event_time is None or (timestamp and timestamp > last_event_time):
            last_event_time = timestamp

        if timestamp and now - timestamp <= timedelta(hours=max_age_hours):
            recent_count += 1

    if not total_count:
        return {
            "user_id": user_id,
            "total_events": 0,
            "recent_events": 0,
            "event_counts": {},
            "errors": [],
            "last_event_time": None
        }

    return {
        "user_id": user_id,
        "total_events": total_count,
        "recent_events": recent_count,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time.isoformat() if last_event_time else None
    }
```

80 t/s, 374 tokens, 5s
