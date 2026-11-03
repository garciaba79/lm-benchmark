# LFM2.5 230M
Model: lfm2.5-230m
Test: Code Fim 1
Created: 11/02/2026, 11:16:38 PM
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
from collections import defaultdict

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
    - "errors": list of error event metadata (or empty list")
    - "last_event_time": ISO string of the most recent event, or None
    
    Handle missing/invalid timestamps and empty input gracefully.
    """
    user_id = str(user_id)
    total_events = 0
    recent_events_count = defaultdict(int)
    errors = []
    last_event_time = None

    for event in events:
        timestamp_str, type, metadata = event['metadata']
        if not isinstance(timestamp_str, datetime):
            continue  # Skip invalid timestamps or empty strings
        
        # Calculate age from timestamp (assuming a reasonable range of 0-24 hours)
        age_range = (max_age_hours - timestamp_str) * 24
        if age_range < 0:
            errors.append(("Invalid age", metadata))
            continue

        user_id += event['timestamp']
        total_events += 1
        recent_events_count[type] += 1
        errors = []
        last_event_time = timestamp_str
        
    # Calculate the most recent timestamp if no events were found
    if not recent_events_count:
        recent_time = None
        user_id += min(max_age_hours, recent_events_count['timestamp'])
    
    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events_count,
        "event_counts": dict(event_type) if event_type else defaultdict(int),
        "errors": errors,
        "last_event_time": last_event_time
    }
```

962 t/s, 532 tokens, 1s
