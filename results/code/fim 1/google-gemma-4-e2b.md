# Gemma 4 E2B
Model: google/gemma-4-e2b
Test: Code Fim 1
Created: 11/15/2026, 09:40:51 PM
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

    if not events:
        return {
            "user_id": user_id,
            "total_events": 0,
            "recent_events": 0,
            "event_counts": {},
            "errors": [],
            "last_event_time": None
        }

    processed_events = []
    error_metadata = []
    
    # Step 1: Parse timestamps and filter for the specific user
    for event in events:
        if event.get("user_id") != user_id:
            continue
        
        timestamp_str = event.get("timestamp")
        if not timestamp_str:
            continue

        try:
            # Parse ISO 8601 string and ensure it's timezone aware (assuming UTC if no TZ info is present, or handling parsing robustly)
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            if dt.tzinfo is None:
                # Attempt to treat naive time as UTC if we can't determine timezone (common in log parsing)
                dt = dt.replace(tzinfo=timezone.utc)
            
            event_time = dt.astimezone(timezone.utc)

            processed_events.append({
                "timestamp": timestamp_str,
                "type": event.get("type"),
                "metadata": event.get("metadata", {})
            })

        except ValueError:
            # Handle invalid timestamp format
            error_metadata.append({"original_event": event, "reason": "Invalid timestamp format"})
            continue
    
    if not processed_events:
        return {
            "user_id": user_id,
            "total_events": 0,
            "recent_events": 0,
            "event_counts": {},
            "errors": error_metadata,
            "last_event_time": None
        }

    # Step 2: Calculate metrics from processed events
    event_counts = {}
    recent_events_count = 0
    last_event_time = None
    
    now = datetime.now(timezone.utc)
    time_threshold = timedelta(hours=max_age_hours)

    for event in processed_events:
        event_type = event["type"]
        
        # Update counts
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Track most recent event
        try:
            current_time = datetime.fromisoformat(event["timestamp"].replace('Z', '+00:00')).astimezone(timezone.utc)
            if last_event_time is None or current_time > last_event_time:
                last_event_time = current_time
        except ValueError:
            # This should ideally not happen if processing was correct, but handle defensively
            pass

        # Check age (using the time of processing for filtering)
        try:
            event_dt = datetime.fromisoformat(event["timestamp"].replace('Z', '+00:00')).astimezone(timezone.utc)
            time_difference = now - event_dt
            if time_difference < time_threshold:
                recent_events_count += 1
        except ValueError:
             # Ignore events with bad timestamps for recent count calculation if they were already filtered out or handled above
             pass


    # Step 3: Format the result
    return {
        "user_id": user_id,
        "total_events": len(processed_events),
        "recent_events": recent_events_count,
        "event_counts": event_counts,
        "errors": error_metadata,
        "last_event_time": last_event_time.isoformat() if last_event_time else None
    }

193 t/s, 918 tokens, 5s
