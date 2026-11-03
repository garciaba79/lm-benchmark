# LFM2.5 350M
Model: lfm2.5-350m
Test: Code Fim 1
Created: 11/02/2026, 11:16:53 PM
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

```
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
    
    filtered = [event for event in events if event["user_id"] == user_id]
    total_events = len(filtered)
    recent_events = max_age_hours * 24  # Convert hours to days

    errors = []
    last_event_time = None

    for event in filtered:
        try:
            timestamp = datetime.fromisoformat(event["timestamp"])
            if last_event_time and (datetime.now().day == last_event_time[0].day):
                continue
            error_type = event["type"]
            errors.append({"error": f"{event['timestamp']} - {error_type}"})
        except:
            errors.append({"error": "Invalid timestamp"})

    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events,
        "event_counts": dict(zip(event["type"], event["count"])}),
        "errors": errors,
        "last_event_time": last_event_time
    }
```

737 t/s, 422 tokens, 1s
