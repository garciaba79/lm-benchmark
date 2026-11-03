# Nvidia NVIDIA Nemotron Nano 9B v2
Model: nvidia_nvidia-nemotron-nano-9b-v2
Test: Code Fim 1
Created: 11/03/2026, 12:46:30 AM
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
    latest_time = None
    current_time = datetime.now(timezone.utc)
    cutoff_time = current_time - timedelta(hours=max_age_hours)
    
    for event in events:
        try:
            ts_str = event['timestamp']
            ts = datetime.fromisoformat(ts_str)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            else:
                ts = ts.astimezone(timezone.utc)
        except (KeyError, ValueError):
            continue
        
        total_events += 1
        if ts >= cutoff_time:
            recent_events += 1
        
        event_type = event['type']
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        if event_type == 'error':
            errors.append(event.get('metadata', {}))
        
        if latest_time is None or ts > latest_time:
            latest_time = ts
    
    last_event_time = latest_time.isoformat() if latest_time else None
    
    return {
        'user_id': user_id,
        'total_events': total_events,
        'recent_events': recent_events,
        'event_counts': event_counts,
        'errors': errors,
        'last_event_time': last_event_time
    }

101 t/s, 5662 tokens, 57s
