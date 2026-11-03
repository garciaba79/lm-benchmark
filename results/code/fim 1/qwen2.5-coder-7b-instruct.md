# Qwen2.5 Coder 7B Instruct
Model: qwen2.5-coder-7b-instruct
Test: Code Fim 1
Created: 11/03/2026, 12:28:30 AM
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
    event_counts = {}
    errors = []
    last_event_time = None
    
    for event in events:
        if 'user_id' not in event or event['user_id'] != user_id:
            continue
        
        try:
            timestamp = datetime.fromisoformat(event['timestamp']).replace(tzinfo=timezone.utc)
        except ValueError:
            continue  # Skip invalid timestamps
        
        if now - timestamp > max_age:
            continue  # Skip events older than max_age_hours
        
        event_type = event.get('type', 'unknown')
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        if event_type == 'error':
            errors.append(event.get('metadata', {}))
        
        last_event_time = timestamp.isoformat()
    
    return {
        "user_id": user_id,
        "total_events": len(events),
        "recent_events": sum(1 for count in event_counts.values()),
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time
    }
```

144 t/s, 492 tokens, 3s
