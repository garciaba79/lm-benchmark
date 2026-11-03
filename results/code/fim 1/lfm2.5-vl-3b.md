# LFM2.5 VL 3B
Model: lfm2.5-vl-3b
Test: Code Fim 1
Created: 11/02/2026, 11:19:44 PM
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
    
    # Filter events for the user, calculate age, aggregate counts,
    # collect errors, and determine the most recent timestamp.
    # Handle missing/invalid timestamps and empty input gracefully.
    
    processed_events = []
    total_events = 0
    event_counts = {}
    errors = []
    last_event_time = None
    
    for event in events:
        if not isinstance(event, dict):
            continue
        
        try:
            ts_str = event["timestamp"]
            dt = datetime.fromisoformat(ts_str).replace(tzinfo=timezone.utc)
            
            if "metadata" in event and not isinstance(event["metadata"], dict):
                errors.append(event)
                continue
            
            user_id_match = any(e.get("user_id") == user_id for e in events)
            if not user_id_match:
                continue
                
            # Calculate age in hours (assuming current time is UTC)
            now = datetime.now(timezone.utc)
            age_hours = (now - dt).total_seconds() / 3600
            
            processed_events.append({
                "timestamp": ts_str,
                "type": event.get("type"),
                "metadata": event.get("metadata")
            })
            
            total_events += 1
            if event.get("type") in event_counts:
                event_counts[event["type"]] += 1
            else:
                event_counts[event["type"]] = 1
            
        except (KeyError, ValueError, TypeError):
            continue
    
    # Determine recent events and last event time
    recent_events = sum(1 for e in processed_events if abs((datetime.fromisoformat(e["timestamp"])).total_seconds() - now.total_seconds()) <= max_age_hours * 3600)
    
    return {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_time.isoformat() if last_event_time else None
    }

287 t/s, 642 tokens, 2s
