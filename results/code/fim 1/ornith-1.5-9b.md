# Ornith 1.5 9B
Model: ornith-1.5-9b
Test: Code Fim 1
Created: 11/03/2026, 12:49:15 AM
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
    
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=max_age_hours)
    
    total_events = 0
    recent_events = 0
    event_counts: dict[str, int] = {}
    errors: list[dict] = []
    last_event_time: datetime | None = None
    
    for event in events:
        if not isinstance(event, dict):
            continue
        
        total_events += 1
        
        # Skip events that don't belong to this user (if a "user_id" field exists)
        if "user_id" in event and str(event["user_id"]) != str(user_id):
            continue
        
        timestamp = None
        try:
            ts = event.get("timestamp")
            if isinstance(ts, datetime):
                timestamp = ts
            elif isinstance(ts, str):
                parsed = datetime.fromisoformat(ts)
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                timestamp = parsed
        except (ValueError, TypeError):
            # Invalid or missing timestamp; skip age-based processing but still count the event
            pass
        
        if timestamp is not None:
            recent_events += 1
            
            if last_event_time is None or timestamp > last_event_time:
                last_event_time = timestamp
        
        event_type = event.get("type")
        if isinstance(event_type, str):
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        if event_type == "error":
            metadata = event.get("metadata", {})
            if not isinstance(metadata, dict):
                metadata = {"raw": metadata}
            errors.append(metadata)
    
    # Format last_event_time as ISO string or None
    if last_event_time is not None:
        if last_event_time.tzinfo is None:
            last_event_time = last_event_time.replace(tzinfo=timezone.utc)
        last_event_time_str = last_event_time.isoformat()
    else:
        last_event_time_str = None
    
    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time_str,
    }
```

162 t/s, 767 tokens, 5s
