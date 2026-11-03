# Qwen3.5 4B
Model: qwen3.5-4b
Test: Code Fim 1
Created: 11/03/2026, 12:20:10 AM
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
    
    # Initialize result structure
    result = {
        "user_id": user_id,
        "total_events": 0,
        "recent_events": 0,
        "event_counts": {},
        "errors": [],
        "last_event_time": None
    }
    
    if not events:
        return result
    
    # Parse timestamps and filter valid ones
    parsed_events = []
    for event in events:
        try:
            ts_str = event.get("timestamp")
            if not ts_str:
                continue
            
            dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
            
            # Check if within max_age_hours (relative to now)
            current_time = datetime.now(timezone.utc)
            age_threshold = current_time - timedelta(hours=max_age_hours)
            
            is_recent = dt >= age_threshold
            
            parsed_events.append({
                "dt": dt,
                "type": event.get("type", ""),
                "metadata": event.get("metadata", {}),
                "is_recent": is_recent
            })
        except (ValueError, TypeError):
            # Skip events with invalid timestamps
            continue
    
    result["total_events"] = len(parsed_events)
    
    if not parsed_events:
        return result
    
    # Aggregate counts and collect errors
    for event in parsed_events:
        etype = event["type"]
        result["event_counts"][etype] = result["event_counts"].get(etype, 0) + 1
        
        if etype == "error":
            metadata = event.get("metadata", {})
            # Append a copy to avoid external mutation issues
            result["errors"].append(metadata.copy())
    
    # Find most recent event time
    if parsed_events:
        max_dt = max(e["dt"] for e in parsed_events)
        result["last_event_time"] = max_dt.isoformat()
    
    # Count recent events (within the threshold, regardless of type)
    result["recent_events"] = sum(1 for e in parsed_events if e["is_recent"])
    
    return result

172 t/s, 663 tokens, 4s
