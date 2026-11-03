# Gemma 4 E4B
Model: google/gemma-4-e4b
Test: Code Fim 1
Created: 11/03/2026, 12:33:22 AM
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

    total_events = 0
    event_counts = {}
    error_metadata: list[dict] = []
    recent_events_count = 0
    last_event_time_dt = None
    valid_events = []

    # Get the current time in UTC for comparison
    now_utc = datetime.now(timezone.utc)
    cutoff_time = now_utc - timedelta(hours=max_age_hours)

    for event in events:
        if not isinstance(event, dict):
            continue
        
        # Basic filtering/validation
        if "user_id" in event and event["user_id"] != user_id:
            continue
        if "timestamp" not in event or "type" not in event:
            continue

        total_events += 1
        event_type = event['type']
        
        # Update event counts
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Handle errors
        if event_type == "error" and isinstance(event.get("metadata"), dict):
            error_metadata.append(event["metadata"])

        # Process timestamp and check for recency/last time
        try:
            # Attempt to parse ISO 8601 string, ensuring timezone awareness (UTC preferred)
            ts_str = event["timestamp"]
            dt = datetime.fromisoformat(ts_str)
            
            # If the parsed datetime is naive, assume it's UTC if no timezone info was present
            if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
                dt = dt.replace(tzinfo=timezone.utc)

            # Update last event time (we compare the datetime objects directly)
            if last_event_time_dt is None or dt > last_event_time_dt:
                last_event_time_dt = dt
                
            # Check recency
            if dt >= cutoff_time and dt <= now_utc:
                recent_events_count += 1

        except ValueError:
            # Skip events with invalid timestamps
            pass
    
    # Format the last event time back to ISO string if one was found
    last_event_time_str = None
    if last_event_time_dt:
        last_event_time_str = last_event_time_dt.isoformat()

    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events_count,
        "event_counts": event_counts,
        "errors": error_metadata,
        "last_event_time": last_event_time_str
    }

144 t/s, 850 tokens, 6s
