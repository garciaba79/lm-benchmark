# LFM2.5 24B A2B
Model: lfm2.5-24b-a2b
Test: Code Fim 1
Created: 11/03/2026, 01:31:53 AM
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
    
    # Filter events for the user
    filtered_events = [ev for ev in events if ev.get("user_id") == user_id]
    
    parsed_events = []  # List of (datetime, event_dict)
    
    for ev in filtered_events:
        ts_str = ev.get("timestamp")
        try:
            # Normalize Z suffix to +00:00 for fromisoformat
            if ts_str.endswith('Z'):
                ts_str = ts_str[:-1] + '+00:00'
            dt = datetime.fromisoformat(ts_str)
            # Ensure timezone-aware
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        except Exception:
            # Skip events with invalid timestamps
            continue
        
        parsed_events.append((dt, ev))
    
    total_events = len(parsed_events)
    
    now = datetime.now(timezone.utc)
    recent_count = 0
    for dt, _ in parsed_events:
        age = now - dt
        if age <= timedelta(hours=max_age_hours):
            recent_count += 1
    
    # Aggregate event type counts
    event_counts = {}
    for _, ev in parsed_events:
        typ = ev.get("type")
        if typ:
            event_counts[typ] = event_counts.get(typ, 0) + 1
    
    # Collect error metadata
    errors = []
    for _, ev in parsed_events:
        if ev.get("type") == "error":
            meta = ev.get("metadata", {})
            if isinstance(meta, dict):
                errors.append(meta)
    
    # Determine most recent event timestamp
    last_event_time = None
    if parsed_events:
        latest_dt = max(parsed_events, key=lambda x: x[0])[0]
        last_event_time = latest_dt.isoformat()
    
    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_count,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time
    }

135 t/s, 4519 tokens, 34s
