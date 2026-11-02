# LFM2.5 2.6B
Model: lfm2.5-2.6b
Test: 
Created: 11/01/2026, 11:27:31 PM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Fixed a bug today in my Home Assistant custom integration for the Wyze cam. The motion detection webhook was failing intermittently because the timestamp format from Wyze API changed (now ISO 8601 with milliseconds). Updated the parser from datetime.strptime('%Y-%m-%d %H:%M:%S') to handle .%f. Also added a try/except block with logging. Tested with a fake event payload—works now. Code change was small but saved a lot of false alerts. Spent about 45 minutes debugging. Reminded myself to check API docs more often when vendors update things.

> #### 🤖 Assistant

Your fix looks solid and well-implemented. Here's a quick summary of why your approach is correct:

**The Issue**
Wyze changed their API timestamp format from `%Y-%m-%d %H:%M:%S` (no milliseconds) to ISO 8601 with milliseconds (`%Y-%m-%dT%H:%M:%S.%f`). This caused the existing parser to fail intermittently, leading to false negatives in motion detection.

**The Fix**
- Updated `datetime.strptime()` to handle the new format (presumably something like `'%Y-%m-%dT%H:%M:%S.%f'` or similar)
- Added try/except with logging for graceful error handling
- Tested with a fake payload to verify

**Why This Works**
1. The parser now matches Wyze's actual response format
2. The exception handling prevents the integration from crashing on unexpected timestamps
3. Logging gives you visibility if edge cases still occur in production

Your 45-minute debugging session was well spent—this kind of API version change is common and can easily break custom integrations. The fix is minimal but targeted, which is exactly right.

One small note: make sure your `datetime` parsing accounts for microseconds properly if you're using `.%f`. If Wyze's timestamp has milliseconds (3 digits) rather than microseconds (6 digits), the format string should use `.%f` which handles both cases correctly in Python 3.7+.

The implementation looks good—this should eliminate those intermittent false alerts.

255 t/s, 709 tokens, 3s, 5%
