# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: Code Fim 1
Created: 11/03/2026, 02:52:12 AM
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
    max_age = timedelta(hours=max_age_hours)
    
    user_events = []
    event_counts = {}
    errors = []
    latest_timestamp = None
    
    for event in events:
        try:
            timestamp = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            
            if latest_timestamp is None or timestamp > latest_timestamp:
                latest_timestamp = timestamp
                
            # Filter for user_id (assuming events have user_id field)
            if event.get("user_id") == user_id:
                user_events.append(event)
                
                # Count event types
                event_type = event["type"]
                event_counts[event_type] = event_counts.get(event_type, 0) + 1
                
                # Collect errors
                if event["type"] == "error":
                    errors.append(event.get("metadata", {}))
                    
        except (ValueError, KeyError):
            # Skip invalid events
            continue
    
    recent_events = 0
    if user_events:
        for event in user_events:
            try:
                timestamp = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(tzinfo=timezone.utc)
                    
                if now - timestamp <= max_age:
                    recent_events += 1
            except (ValueError, KeyError):
                continue
    
    return {
        "user_id": user_id,
        "total_events": len(user_events),
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": latest_timestamp.isoformat() if latest_timestamp else None
    }

61 t/s, 468 tokens, 8s
