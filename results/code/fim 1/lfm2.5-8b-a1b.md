# LFM2.5 8B A1B
Model: lfm2.5-8b-a1b
Test: Code Fim 1
Created: 11/03/2026, 12:41:08 AM
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
    from datetime import datetime, timezone

    def parse_iso(s):
        try:
            if s.endswith('Z'):
                s = s[:-1] + '+00:00'
            return datetime.fromisoformat(s)
        except Exception:
            return None

    now = datetime.now(timezone.utc)
    recent_count = 0
    event_counts = {}
    errors_meta = []
    valid_events = []

    for ev in events:
        typ = ev.get('type')
        if not typ:
            continue
        event_counts[typ] = event_counts.get(typ, 0) + 1

        meta = ev.get('metadata')
        if typ == 'error' and meta is not None:
            errors_meta.append(meta)

        dt = parse_iso(ev['timestamp'])
        valid_events.append((dt, ev))

    max_dt_event = None
    for dt, _ in valid_events:
        if dt is not None and (max_dt_event is None or dt > max_dt_event):
            max_dt_event = dt

    last_event_time = max_dt_event.isoformat() if max_dt_event else None

    return {
        "user_id": user_id,
        "total_events": len(events),
        "recent_events": recent_count,
        "event_counts": event_counts,
        "errors": errors_meta,
        "last_event_time": last_event_time
    }

388 t/s, 1828 tokens, 5s
