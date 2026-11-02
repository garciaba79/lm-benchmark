# Ornith 1.5 9B
Model: ornith-1.5-9b
Test: 
Created: 11/01/2026, 11:27:31 PM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Fixed a bug today in my Home Assistant custom integration for the Wyze cam. The motion detection webhook was failing intermittently because the timestamp format from Wyze API changed (now ISO 8601 with milliseconds). Updated the parser from datetime.strptime('%Y-%m-%d %H:%M:%S') to handle .%f. Also added a try/except block with logging. Tested with a fake event payload—works now. Code change was small but saved a lot of false alerts. Spent about 45 minutes debugging. Reminded myself to check API docs more often when vendors update things.

> #### 🤖 Assistant

Nice catch—timestamp format drift from third-party APIs is one of the most common integration breakages, and your instinct to add defensive parsing plus logging was exactly right for this kind of intermittent failure.

A few things worth considering as you refine it:

**1. Consider `datetime.fromisoformat()` instead of strptime guessing.**
strptime forces you to match an exact format string, which is fragile the next time Wyze changes formats again. `fromisoformat()` parses ISO 8601 natively (fractional seconds and timezone offsets included). Caveat: its robustness was significantly expanded in Python 3.11—verify against Home Assistant's minimum supported Python version before relying on it fully, since older versions don't handle everything (e.g., a trailing `Z`). A safe pattern is try `fromisoformat()` first, fall back to your strptime as needed.

**2. Watch the separator and timezone.**
ISO 8601 uses `T` between date and time rather than a space, and Wyze often appends a UTC designator like `Z` or `+00:00`. If some events still arrive with those variants while others use your new format, that would explain the "intermittent" behavior. Logging the raw value before parsing makes this easy to spot next time—worth confirming you're capturing it.

**3. Turn the fake payload into a regression test.**
Since you tested manually, consider committing that as an actual test (Home Assistant has a testing framework). That way the next format change fails loudly in CI instead of silently causing false alerts again.

Your takeaway about checking API docs is well earned—Wyze's public API isn't heavily documented, so defensive parsing is genuinely good practice for anything depending on third-party endpoints.

117 t/s, 2829 tokens, 24s, 18%
