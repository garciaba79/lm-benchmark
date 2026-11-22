# Qwen3.6 35B A3B
Model: qwen/qwen3.6-35b-a3b
Test: Code Fim 1
Created: 11/22/2026, 03:12:51 AM
Exported from: LM Studio (via test script)
Context 16K

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
    
    # Filter events for the user, calculate age, aggregate counts,
    # collect errors, and determine the most recent timestamp.
    # Handle missing/invalid timestamps and empty input gracefully.
    
    user_events = [e for e in events if e.get("user_id") == user_id]
    
    total_events = len(user_events)
    event_counts = {}
    errors = []
    recent_events = 0
    last_event_time = None
    
    now = datetime.now(timezone.utc)
    cutoff_time = now - timedelta(hours=max_age_hours)
    
    for event in user_events:
        # Aggregate event counts
        event_type = event.get("type")
        if event_type:
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Collect error metadata
        if event_type == "error":
            metadata = event.get("metadata")
            if metadata is not None:
                errors.append(metadata)
        
        # Parse timestamp and check recency
        timestamp_str = event.get("timestamp")
        if timestamp_str:
            try:
                # Handle various ISO 8601 formats
                ts = datetime.fromisoformat(timestamp_str)
                # If naive, assume UTC
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                
                # Check if event is within max_age_hours
                if ts >= cutoff_time:
                    recent_events += 1
                
                # Track the most recent event
                if last_event_time is None or ts > last_event_time:
                    last_event_time = ts
            except (ValueError, TypeError):
                # Invalid timestamp, skip for recency and last_event_time
                pass
    
    # Format last_event_time back to ISO string
    if last_event_time is not None:
        last_event_str = last_event_time.isoformat()
    else:
        last_event_str = None
    
    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_str
    }

43 t/s, 686 tokens, 16s, 6%
