# Falcon H1R 7B
Model: falcon-h1r-7b
Test: Code Fim 1
Created: 11/03/2026, 12:22:29 AM
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
    
    # Initialize aggregates
    total_events = 0
    recent_events = 0
    event_counts: dict[str, int] = {}
    errors: list[dict] = []
    last_event_dt: datetime | None = None
    
    # Current UTC time for age calculations
    now = datetime.now(timezone.utc)
    
    for ev in events:
        # Ensure we have a dictionary and the required fields
        if not isinstance(ev, dict):
            continue
        
        uid = ev.get("user_id")
        if uid is None or uid != user_id:
            continue
        
        timestamp_str = ev.get("timestamp")
        event_type = ev.get("type", "")
        
        # Safely parse the ISO timestamp; skip invalid ones
        try:
            dt = datetime.fromisoformat(timestamp_str)
        except Exception:
            # Invalid or missing timestamp, ignore this event for aggregation
            continue
        
        # Count total events and recent ones based on age window
        total_events += 1
        if now - dt <= timedelta(hours=max_age_hours):
            recent_events += 1
        
        # Update counts per event type
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Track the most recent event timestamp
        if last_event_dt is None or dt > last_event_dt:
            last_event_dt = dt
        
        # Collect error metadata if the type indicates an error
        if event_type.lower() == "error":
            # Include only non‑timestamp/non‑type fields as metadata
            errors.append({k: v for k, v in ev.items() if k not in ("timestamp", "type")})
    
    # Prepare the final output dictionary
    last_event_time: str | None = None
    if last_event_dt is not None:
        try:
            last_event_time = last_event_dt.isoformat()
        except Exception:
            pass
    
    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time,
    }

102 t/s, 4425 tokens, 44s
