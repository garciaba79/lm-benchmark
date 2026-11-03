# Qwen3.8 27B
Model: qwen/qwen3.8-27b
Test: Code Fim 1
Created: 11/03/2026, 01:41:46 AM
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
    
    result = {
        "user_id": user_id,
        "total_events": 0,
        "recent_events": 0,
        "event_counts": {},
        "errors": [],
        "last_event_time": None
    }
    
    if not events:
        return result
    
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=max_age_hours)
    
    latest_dt = None
    latest_iso = None
    
    for event in events:
        if not isinstance(event, dict):
            continue
        
        # Check if event belongs to the user
        event_user = event.get("user_id", user_id)
        if event_user != user_id:
            continue
        
        event_type = event.get("type", "unknown")
        timestamp_str = event.get("timestamp")
        metadata = event.get("metadata", {})
        
        # Count this event
        result["total_events"] += 1
        
        # Count by type
        result["event_counts"][event_type] = result["event_counts"].get(event_type, 0) + 1
        
        # Collect errors
        if event_type == "error":
            result["errors"].append(metadata if metadata else {})
        
        # Parse timestamp
        parsed_dt = None
        if timestamp_str:
            try:
                ts = timestamp_str
                # Handle Z suffix
                if ts.endswith("Z"):
                    ts = ts[:-1] + "+00:00"
                parsed_dt = datetime.fromisoformat(ts)
                # Ensure timezone-aware
                if parsed_dt.tzinfo is None:
                    parsed_dt = parsed_dt.replace(tzinfo=timezone.utc)
            except (ValueError, TypeError):
                parsed_dt = None
        
        if parsed_dt is not None:
            # Check if recent
            if parsed_dt >= cutoff:
                result["recent_events"] += 1
            
            # Track latest
            if latest_dt is None or parsed_dt > latest_dt:
                latest_dt = parsed_dt
                latest_iso = timestamp_str
    
    result["last_event_time"] = latest_iso
    return result
```

22 t/s, 671 tokens, 31s
