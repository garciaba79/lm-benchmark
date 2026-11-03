# Qwen2.5 Coder 32B Instruct
Model: qwen2.5-coder-32b-instruct
Test: Code Fim 1
Created: 11/03/2026, 03:07:02 AM
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

def process_user_events(events: list[dict], user_id: str, max_age_hours: int = 24) -> dict:
    from datetime import datetime, timezone, timedelta
    
    total_events = 0
    recent_events = 0
    event_counts = {}
    errors = []
    last_event_time = None
    
    current_time = datetime.now(timezone.utc)
    
    for event in events:
        if event.get('user_id') != user_id:
            continue
        
        total_events += 1
        timestamp_str = event.get('timestamp')
        
        try:
            timestamp = datetime.fromisoformat(timestamp_str).astimezone(timezone.utc)
        except (TypeError, ValueError):
            continue
        
        if last_event_time is None or timestamp > last_event_time:
            last_event_time = timestamp
        
        age = current_time - timestamp
        if age <= timedelta(hours=max_age_hours):
            recent_events += 1
        
        event_type = event.get('type')
        if event_type in event_counts:
            event_counts[event_type] += 1
        else:
            event_counts[event_type] = 1
        
        if event_type == 'error':
            errors.append(event.get('metadata', {}))
    
    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time.isoformat() if last_event_time else None
    }

6 t/s, 315 tokens, 51s
