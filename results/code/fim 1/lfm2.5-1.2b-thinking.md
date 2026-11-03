# LFM2.5 1.2B Thinking
Model: lfm2.5-1.2b-thinking
Test: Code Fim 1
Created: 11/02/2026, 11:17:38 PM
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
def process_user_events(events, user_id, max_age_hours=24):
    T = max_age_hours * 3600
    current_utc = datetime.datetime.utcnow()
    valid_events = []
    for e in events:
        if e['user_id'] == user_id:
            try:
                e_time = datetime.datetime.fromisoformat(e['timestamp'])
                diff = abs((current_utc - e_time).total_seconds()
            except:
                continue
            if diff <= T:
                valid_events.append(e)
    counts = defaultdict(int)
    for e in valid_events:
        counts[e['type']] += 1
    errors = [e['metadata'] for e in valid_events if e['type'] == 'error']
    last_event_time = max(valid_events, key=lambda x: x['timestamp']) if valid_events else None
    return {
        "user_id": user_id,
        "total_events": len(valid_events),
        "recent_events": last_event_time,
        "event_counts": dict(counts),
        "errors": errors,
        "last_event_time": last_event_time
    }
```

521 t/s, 6756 tokens, 13s
