# Qwen3 14B
Model: qwen/qwen3-14b
Test: Code Fim 1
Created: 11/03/2026, 01:05:48 AM
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

    # Initialize result dictionary
    result = {
        "user_id": user_id,
        "total_events": 0,
        "recent_events": 0,
        "event_counts": {},
        "errors": [],
        "last_event_time": None
    }

    # Get current time in UTC
    now = datetime.now(timezone.utc)

    # Process each event
    for event in events:
        # Validate and parse timestamp
        if not isinstance(event, dict) or "timestamp" not in event:
            continue

        try:
            timestamp_str = event["timestamp"]
            event_time = datetime.fromisoformat(timestamp_str).replace(tzinfo=timezone.utc)
        except (ValueError, KeyError):
            continue

        # Calculate age of the event
        age_hours = (now - event_time).total_seconds() / 3600

        # Increment total events count
        result["total_events"] += 1

        # Update event counts
        event_type = event.get("type", "unknown")
        if event_type in result["event_counts"]:
            result["event_counts"][event_type] += 1
        else:
            result["event_counts"][event_type] = 1

        # Check if event is recent (within max_age_hours)
        if age_hours <= max_age_hours:
            result["recent_events"] += 1

        # Track the most recent event time
        if result["last_event_time"] is None or event_time > datetime.fromisoformat(result["last_event_time"]).replace(tzinfo=timezone.utc):
            result["last_event_time"] = timestamp_str

        # Collect error metadata
        if event_type == "error" and "metadata" in event:
            result["errors"].append(event["metadata"])

    return result
```

78 t/s, 571 tokens, 7s
