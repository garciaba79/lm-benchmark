# Deepseek Coder 6.7B Instruct
Model: deepseek-coder-6.7b-instruct
Test: Code Fim 1
Created: 11/03/2026, 12:38:29 AM
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
    
    filtered = [e for e in events if 'timestamp' in e and 'type' in e]  # Filter out invalid event dictionaries.
    user_events = [e for e in filtered if (e['user'] == user_id)]       # Filter by the given user id.
    
    total_events = len(user_events)                                    # Total events count.
  
    recent_age = datetime.now() - timedelta(hours=max_age_hours)        # Calculate age limit for "recent" events.
    recent_events = [e for e in user_events if (datetime.fromisoformat(e['timestamp']) > recent_age)]  # Filter by age.
  
    event_counts = {}                                                   # Initialize counts dictionary.
    errors = []                                                         # Initialize error list.
    
    for e in user_events:                                                # Count events and collect errors.
        if 'metadata' in e and e['type'] == "error":                      # Check for metadata and event type match.
            errors.append(e['metadata'])                                  # Append to the error list.
        
        event_counts[e['type']] = event_counts.get(e['type'], 0) + 1     # Increment count in dictionary.
  
    last_event_time = max([datetime.fromisoformat(e['timestamp']) for e in user_events], default=None) if user_events else None
  
    return {                                                             # Return the summary as a dict.
        "user_id": user_id, 
        "total_events": total_events, 
        "recent_events": len(recent_events), 
        "event_counts": event_counts, 
        "errors": errors, 
        "last_event_time": last_event_time.isoformat() if last_event_time else None
    }

150 t/s, 491 tokens, 3s
