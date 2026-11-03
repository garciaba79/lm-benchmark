# Rnj 1
Model: essentialai/rnj-1
Test: Code Fim 1
Created: 11/03/2026, 12:44:28 AM
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
    
    # Initialize summary dictionary
    summary = {
        "user_id": user_id,
        "total_events": 0,
        "recent_events": 0,
        "event_counts": {},
        "errors": [],
        "last_event_time": None
    }
    
    # Calculate the cutoff time for recent events
    now = datetime.now(timezone.utc)
    max_age_timedelta = timedelta(hours=max_age_hours)
    cutoff_time = now - max_age_timedelta
    
    # Process each event
    for event in events:
        try:
            # Parse the timestamp
            event_time = datetime.fromisoformat(event["timestamp"]).replace(tzinfo=timezone.utc)
            
            # Update total events count
            summary["total_events"] += 1
            
            # Check if the event is recent and update recent events count
            if event_time >= cutoff_time:
                summary["recent_events"] += 1
                
            # Count by event type
            event_type = event.get("type", "unknown")
            if event_type not in summary["event_counts"]:
                summary["event_counts"][event_type] = 0
            summary["event_counts"][event_type] += 1
            
            # Collect error events metadata
            if event_type == "error":
                summary["errors"].append(event.get("metadata", {}))
            
            # Update the most recent event time
            if (summary["last_event_time"] is None) or (event_time > datetime.fromisoformat(summary["last_event_time"]).replace(tzinfo=timezone.utc)):
                summary["last_event_time"] = event["timestamp"]
                
        except (KeyError, ValueError):
            # Skip events with missing/invalid timestamps
            continue
    
    return summary
```

125 t/s, 552 tokens, 5s
