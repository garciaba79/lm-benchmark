# Qwen3.5 9B
Model: qwen/qwen3.5-9b
Test: Code Fim 1
Created: 11/03/2026, 12:51:43 AM
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
    
    now = datetime.now(timezone.utc)
    cutoff_time = now - timedelta(hours=max_age_hours)
    
    total_events = 0
    recent_events = 0
    event_counts: dict[str, int] = {}
    error_list: list[dict] = []
    last_event_time_iso = None
    
    for event in events:
        timestamp_str = event.get("timestamp")
        if not timestamp_str or not isinstance(timestamp_str, str):
            continue
        
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            continue
        
        total_events += 1
        event_type = event.get("type", "unknown")
        
        if event_type not in event_counts:
            event_counts[event_type] = 0
        event_counts[event_type] += 1
        
        if dt >= cutoff_time:
            recent_events += 1
        
        last_event_time_iso = timestamp_str
        
        if event_type == "error":
            metadata = event.get("metadata", {})
            error_list.append(metadata)
    
    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": error_list,
        "last_event_time": last_event_time_iso
    }

119 t/s, 428 tokens, 4s
