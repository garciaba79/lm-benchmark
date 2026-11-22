# Evaluation Results

## Summary

Test evaluated five small local models plus five new larger ones on completing a Python event processing function under strict output constraints. All models produced code with logical errors in filtering, timestamp handling, and aggregation; larger models like qwen3.5-4b and falcon-h1r-7b showed better structure and instruction following but none delivered fully correct or immediately usable implementations. New models showed similar patterns with persistent user filtering and recent event logic issues.

## Key takeaways

- All outputs contained bugs in timestamp handling, user filtering, and aggregation logic.
- Smaller models ran faster but produced more malformed code.
- Instruction following was weak across the board due to extra text or incorrect return keys.
- No model handled empty input or invalid timestamps gracefully as requested.
- Larger models improved cleanliness and partial correctness but still failed core requirements.
- New models continued to assume user_id field in events despite prompt omission.

## Practical notes

- Results require heavy editing or full rewrite before use, negating speed advantages.
- Faster models (900+ t/s) still need substantial developer time to fix.
- None are production-ready without major corrections to core logic.
- Models around 250 t/s offer the best balance of speed and editability among the batch.
- Newer 6-8B models offer marginal quality gains but still demand significant fixes for user filtering and recency.

## Additional notes

- All models ignored the strict 'only output the completed function' instruction to varying degrees.
- Context was unknown for all runs, potentially affecting consistency.
- Several new models assumed user_id field in events despite prompt omission.
- deepseek and granite handled timestamps better than most but still failed user filtering.

## Results

| Model | t/s | Correctness | Quality | Task understanding | Instruction following | Usefulness | Faithfulness | Pros | Cons | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nvidia_nvidia-nemotron-nano-9b-v2 | 101 | 65 | 80 | 70 | 85 | 60 | 80 | Clean function-only output with solid timestamp parsing and empty input handling. | No user filtering and recent_events increments for every parsed event regardless of cutoff. | last_event_time uses latest parsed ts but total_events counts all valid timestamps. |
| lfm2.5-2.6b | 253 | 65 | 75 | 70 | 80 | 60 | 75 | Clean function output with solid error handling and structure. | Incorrect user filtering assuming user_id in events and recent window based on max_ts. | Best overall among new models for editability. |
| openai/gpt-oss-20b | 198 | 60 | 75 | 70 | 75 | 55 | 70 | No user_id assumption and solid timestamp parsing with Z handling. | total_events incremented before timestamp validation and recent_events skips invalid ts. | Produced clean function without markdown wrapper. |
| qwen/qwen3.5-9b | 119 | 60 | 75 | 65 | 85 | 55 | 75 | Clean output, proper empty handling, and Z-suffix timestamp support. | last_event_time set to last processed string instead of most recent and no user filtering. | total_events only counts events with valid timestamps. |
| qwen2.5-coder-32b-instruct | 6 | 60 | 75 | 65 | 80 | 55 | 70 | Clean direct output and proper user_id filtering with Z handling. | Assumed user_id field in events and last_event_time uses parsed datetime. | total_events incremented only for matching user events. |
| falcon-h1r-7b | 102 | 60 | 65 | 65 | 85 | 55 | 75 | Correctly implemented user_id filtering from events and graceful error handling. | Assumed user_id field in events contrary to prompt and produced very long output. | Parsing skipped Z suffix handling and used broad except clauses. |
| qwen/qwen3-14b | 78 | 55 | 70 | 60 | 65 | 50 | 60 | Avoided assuming user_id field and handled Z timestamps reasonably. | last_event_time update logic is inefficient and total_events counts before full validation. | Wrapped in markdown code block violating strict output instruction. |
| qwen/qwen3.8-27b | 22 | 55 | 70 | 60 | 60 | 50 | 55 | Solid timestamp parsing with Z handling and clean structure. | Assumed user_id field in events and wrapped output in markdown. | total_events counts after user filter but recent_events uses parsed cutoff correctly. |
| nvidia/nemotron-3-nano-4b | 225 | 55 | 65 | 60 | 85 | 50 | 70 | Clean output and proper user_id filtering. | Errors list populated with invalid events instead of only error-type metadata. | last_event_time not converted to ISO format in return. |
| google/gemma-4-e4b | 144 | 55 | 60 | 60 | 85 | 50 | 65 | Handled user filtering, error metadata, and timezone-aware timestamps reasonably. | Assumed user_id present in events and total_events counted before full validation. | Included recent check against both cutoff and now but skipped some invalid timestamp cases silently. |
| qwen2.5-coder-1.5b-instruct | 297 | 55 | 60 | 65 | 50 | 50 | 55 | Closest to correct structure with proper filtering and counts. | total_events used unfiltered length and last_event_time logic is broken. | Slowest but most readable code among the batch. |
| granite-4.1-8b | 124 | 50 | 70 | 60 | 85 | 45 | 75 | Good timestamp parsing with Z handling and clean code structure. | Assumed user_id field in events and did not filter by user at all. | last_event_time update logic works but total/recent counts ignore user constraint. |
| qwen3.5-4b | 172 | 50 | 70 | 60 | 90 | 45 | 70 | Strictly followed output format with clean readable code. | Ignored user_id filtering entirely and counted only parsed events. | Used current time for recency without user-specific event filtering. |
| qwen/qwen3-coder-30b | 61 | 50 | 65 | 55 | 70 | 45 | 60 | Direct function output without markdown and reasonable error skipping. | Assumed user_id field and duplicated timestamp parsing logic. | recent_events recount uses separate loop after initial filter. |
| google/gemma-4-e2b | 193 | 50 | 60 | 55 | 75 | 45 | 65 | Direct function output and robust timestamp parsing with error collection. | Assumed user_id field and errors list contains non-metadata entries. | recent count uses processing time instead of cutoff for some checks. |
| google/gemma-4-12b | 81 | 50 | 55 | 60 | 40 | 45 | 50 | Good timestamp parsing with Z handling and error collection. | Included full docstring and filtered by non-existent user_id field. | recent_count uses timedelta comparison but skips invalid timestamps silently. |
| lfm2.5-24b-a2b | 135 | 45 | 65 | 55 | 50 | 40 | 45 | Proper user_id filtering attempt and good Z-suffix normalization. | Assumed user_id field present and produced excessively long output with extra comments. | last_event_time returned without timezone info in some cases. |
| deepseek-coder-6.7b-instruct | 150 | 45 | 60 | 55 | 70 | 40 | 65 | Clean function-only output with reasonable structure and error handling. | Assumed non-existent 'user' field for filtering and used naive datetime.now without timezone. | Recent events used local now instead of UTC cutoff. |
| ornith-1.5-9b | 162 | 45 | 50 | 55 | 30 | 40 | 35 | Detailed edge-case handling and type checks in code. | Wrapped in markdown code block and assumed user_id field for filtering. | recent_events incremented for every event with timestamp, ignoring cutoff. |
| qwen/qwen2.5-coder-14b | 77 | 45 | 50 | 55 | 25 | 40 | 35 | Attempted user filtering and graceful timestamp error handling. | Wrapped in markdown and filtered by non-existent user_id field. | recent_events calculated inside per-event now comparison inside try block. |
| ministral-3-3b-reasoning-2512 | 180 | 45 | 35 | 60 | 20 | 35 | 25 | Included detailed edge case handling in code. | Added long explanation text before the function. | Did not filter events by user_id at all. |
| microsoft/phi-4 | 80 | 40 | 65 | 55 | 70 | 40 | 55 | Clean structure with reasonable error handling for invalid timestamps. | Incorrectly filtered on non-existent user_id field and last_event_time comparison flawed. | Skipped returning early for empty input as some paths returned partial dicts. |
| ministral-3-3b-instruct-2512 | 230 | 40 | 55 | 55 | 50 | 40 | 45 | Reasonable structure and empty input handling. | Wrapped output in markdown code block violating instructions. | Skipped non-recent events entirely from totals. |
| ministral-3-8b-instruct-2512 | 124 | 40 | 55 | 55 | 40 | 35 | 45 | Solid empty input handling and timezone-aware timestamp parsing. | Wrapped in markdown code block and performed no user filtering. | Counts all events regardless of user_id. |
| qwen2.5-coder-7b-instruct | 144 | 40 | 50 | 55 | 30 | 35 | 40 | Attempted proper recent filtering and error collection. | Wrapped output in markdown code block and used incorrect total_events and recent_events calculations. | Skipped older events from all counts instead of separating recent only. |
| deepseek-v4-pro-qwen3.5-9b-uncensored-heretic | 157 | 35 | 55 | 45 | 80 | 30 | 50 | Direct function output with clean structure and Z handling. | No user_id filtering at all and counts all events regardless of user. | last_event_time tracks most recent across all events. |
| mamba-codestral-7b-v0.1 | 148 | 35 | 55 | 50 | 80 | 30 | 60 | Produced compact function-only output with basic structure. | No user_id filtering and flawed last_event_time and recent_events logic. | Assumed all events belong to the target user and used naive timestamp comparisons. |
| essentialai/rnj-1 | 125 | 35 | 50 | 50 | 35 | 30 | 40 | Attempted cutoff logic and error collection with try/except. | Wrapped in markdown, ignored user filtering, and last_event_time update has parsing bug. | total_events incremented before any validation. |
| lfm2.5-1.2b-instruct | 529 | 35 | 40 | 50 | 45 | 35 | 40 | Better organized code with some correct aggregation. | Flawed user matching and recent event filtering logic. | Returned early in some paths, skipping required fields. |
| liquid/lfm2-24b-a2b | 146 | 30 | 50 | 45 | 60 | 30 | 50 | Compact output with basic type checks. | Filtered only on event type instead of user and set recent_events equal to total filtered. | Ignored user_id entirely and used naive age calculation without proper cutoff. |
| lfm2.5-vl-3b | 287 | 30 | 40 | 45 | 70 | 30 | 50 | Followed output format without extra text. | Broken recent_events calculation and uninitialized last_event_time. | Used now incorrectly for age checks. |
| lfm2.5-8b-a1b | 388 | 25 | 40 | 45 | 55 | 25 | 40 | Fast generation and attempted parse helper for timestamps. | No user filtering, recent_count always zero, and total_events uses all events. | Output much longer than requested with unused valid_events list. |
| lfm2.5-1.2b-thinking | 521 | 25 | 30 | 40 | 35 | 25 | 30 | Included defaultdict for counts. | Syntax error and incorrect recent_events field value. | Longer output time despite similar size to instruct variant. |
| lfm2.5-350m | 737 | 20 | 25 | 35 | 30 | 20 | 25 | Attempted basic filtering structure. | Incorrect recent_events calculation and broken return values. | Used undefined variables and wrong datetime logic. |
| lfm2.5-230m | 962 | 15 | 20 | 30 | 25 | 15 | 20 | Extremely fast generation speed. | Code has multiple syntax and logic errors making it unusable. | Output included extra imports and docstring changes not requested. |
