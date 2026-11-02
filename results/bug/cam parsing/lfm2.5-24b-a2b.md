# LFM2.5 24B A2B
Model: lfm2.5-24b-a2b
Test: 
Created: 11/01/2026, 11:27:31 PM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Fixed a bug today in my Home Assistant custom integration for the Wyze cam. The motion detection webhook was failing intermittently because the timestamp format from Wyze API changed (now ISO 8601 with milliseconds). Updated the parser from datetime.strptime('%Y-%m-%d %H:%M:%S') to handle .%f. Also added a try/except block with logging. Tested with a fake event payload—works now. Code change was small but saved a lot of false alerts. Spent about 45 minutes debugging. Reminded myself to check API docs more often when vendors update things.

> #### 🤖 Assistant

That was a smart fix—switching the parser to accept millisecond precision resolves the intermittent webhook failures when Wyze updated their timestamp format. In Python, `datetime.strptime` uses `.%f` for fractional seconds (microseconds), so updating your format string from `'%Y-%m-%d %H:%M:%S'` to something like `'%Y-%m-%d %H:%M:%S.%f'` will correctly parse the ISO 8601 timestamps with milliseconds.

The added try/except block with logging is a good practice—it makes silent timestamp-related failures visible and easier to track down in production. Testing with a fake event payload before redeploying was exactly the right move; it helped confirm that the new parser handles both old and new formats without breaking the integration.

For future API changes, you might consider building a small helper that tries multiple format strings (e.g., ISO 8601 first, then your original fallback) or using `dateutil.parser` with strict settings to avoid silently mis-parsing. That way similar breakages get caught in code review rather than during debugging.

Overall, the 45-minute fix likely saved a lot of noise for users—well done on catching and resolving it so cleanly.

97 t/s, 1263 tokens, 14s, 9%
