# GPT-OSS 20B
Model: openai/gpt-oss-20b
Test: Code Fim 1
Created: 11/03/2026, 01:17:36 AM
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
    
    # Helper to parse ISO 8601 timestamps safely
    def _parse_ts(ts_str):
        try:
            if ts_str.endswith('Z'):
                ts_str = ts_str.replace('Z', '+00:00')
            return datetime.fromisoformat(ts_str).astimezone(timezone.utc)
        except Exception:
            return None
    
    now_utc = datetime.now(timezone.utc)
    recent_delta = timedelta(hours=max_age_hours)
    
    total_events = 0
    recent_events = 0
    event_counts: dict[str, int] = {}
    errors: list[dict] = []
    last_event_ts: datetime | None = None
    
    for ev in events:
        # Count all provided events regardless of validity of timestamp
        total_events += 1
        
        ts_raw = ev.get("timestamp")
        ts = _parse_ts(ts_raw) if ts_raw else None
        if not ts:
            continue  # skip invalid or missing timestamps for further metrics
        
        # Update most recent event time
        if last_event_ts is None or ts > last_event_ts:
            last_event_ts = ts
        
        # Check recency
        if now_utc - ts <= recent_delta:
            recent_events += 1
        
        # Count event type
        etype = ev.get("type", "unknown")
        event_counts[etype] = event_counts.get(etype, 0) + 1
        
        # Collect error metadata
        if etype == "error":
            errors.append(ev.get("metadata", {}))
    
    result: dict[str, any] = {
        "user_id": user_id,
        "total_events": total_events,
        "recent_events": recent_events,
        "event_counts": event_counts,
        "errors": errors,
        "last_event_time": last_event_ts.isoformat() if last_event_ts else None
    }
    
    return result

198 t/s, 722 tokens, 4s
