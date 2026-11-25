# Evaluation Results

## Summary

Tested five small local models on a code completion task to implement a user event processing function, plus five new models. All models produced flawed code with logic errors, incorrect filtering, and instruction violations, though larger models showed better structure and partial correctness. New 27-32B models improved correctness and direct function output but still included docstrings or minor logic issues. The three newest models (9B-35B) showed strong timestamp handling and structure but two skipped user_id filtering while the 35B model performed best overall on correctness.

## Key takeaways

- No model produced a fully correct or clean implementation.
- Smaller models had severe syntax and logic bugs.
- Larger models followed the function signature better but still failed core requirements.
- All outputs violated the strict 'only the function' instruction.
- Speed was high across the board but did not correlate with quality.
- Newer 2-4B models improved on filtering and edge cases but retained docstrings and user_id mismatches.
- 27B+ models achieved higher correctness with direct function starts and better timestamp handling.
- Two of the three newest models ignored the user_id filter entirely despite explicit requirements.

## Practical notes

- None of the outputs are usable without heavy rewriting.
- High t/s means quick generation but edit time would be long due to bugs.
- Best case is using outputs as rough scaffolding then fixing logic manually.
- Smaller models are too broken for any practical coding assistance.
- 2.6B+ models reduce edit time slightly but still require substantial fixes for production use.
- Larger models like qwen2.5-coder-32b-instruct offer the best starting point with fewer edits needed.
- qwen/qwen3.6-35b-a3b provides the strongest new scaffolding for correctness with minimal logic fixes required.

## Additional notes

- All models ignored the 'no extra text' rule and included docstrings or wrappers.
- Timestamp handling and user filtering were consistently mishandled.
- qwen2.5-coder-1.5b was the least broken but still required major fixes.
- nemotron-3-nano-4b came closest to the 'only function' output format.
- qwen2.5-coder-32b-instruct produced the cleanest and most correct logic among all tested.
- qwen/qwen3.6-35b-a3b is the strongest new model for user filtering and overall correctness.

## Results

| Model | t/s | Correctness | Quality | Task understanding | Instruction following | Usefulness | Faithfulness | Pros | Cons | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qwen2.5-coder-32b-instruct | 6 | 85 | 75 | 90 | 65 | 80 | 60 | Clean direct function with correct filtering, recent count, and error handling. | Slow generation speed compared to smaller models. | Highest overall correctness and closest to usable without major rewrites. |
| qwen/qwen3.6-35b-a3b | 43 | 85 | 70 | 90 | 40 | 75 | 45 | Correct user_id filtering with solid logic and timestamp handling. | Includes full docstring violating the only-function rule. | One of the better implementations for correctness among tested models. |
| qwen/qwen3-coder-30b | 61 | 80 | 70 | 90 | 60 | 75 | 55 | Direct function start with accurate user filtering and timestamp parsing. | latest_timestamp calculated before user filter in some paths. | One of the better format-compliant outputs with solid correctness. |
| qwen/qwen3.8-27b | 22 | 75 | 60 | 85 | 30 | 65 | 35 | Solid user_id filtering, Z handling, and correct recent/last_event logic. | Includes full docstring violating the only-function rule. | Strong logic among larger models despite format violation. |
| google/gemma-4-12b | 81 | 70 | 65 | 85 | 35 | 60 | 40 | Proper user_id filter and correct recent count with Z handling. | Includes full docstring and latest_ts may be None on return. | One of the stronger new outputs for filtering logic. |
| google/gemma-4-e2b | 193 | 70 | 65 | 85 | 55 | 70 | 50 | Direct function with robust timestamp parsing and user filtering. | Redundant processing loops and extra error_metadata for invalid timestamps. | Fast and reasonably correct but includes unnecessary complexity. |
| granite-4.1-8b | 124 | 70 | 60 | 85 | 30 | 60 | 35 | Correct user_id filtering, robust timestamp parsing with Z handling, and clean aggregation. | Includes full docstring violating the only-function rule. | Best correctness among new models but still needs edits for format and recent count. |
| lfm2.5-24b-a2b | 135 | 70 | 55 | 85 | 30 | 55 | 35 | Strong user_id filtering, Z handling, and correct recent logic. | Includes full docstring and extremely long output. | Best correctness among new models but violates format rule. |
| microsoft/phi-4 | 80 | 65 | 60 | 80 | 35 | 55 | 40 | Includes user_id filter and handles Z timestamps reasonably. | last_event_time comparison has None bug and returns datetime object. | Good filtering but needs fixes for return type and edge cases. |
| falcon-h1r-7b | 102 | 65 | 55 | 80 | 35 | 55 | 40 | Properly filters by user_id and handles most aggregation correctly. | Includes full docstring and has timezone parsing issues. | Very long output; recent check assumes naive datetimes. |
| google/gemma-4-e4b | 144 | 60 | 65 | 80 | 35 | 55 | 40 | Strong user_id filtering and correct recent event cutoff logic. | Includes full docstring and counts total_events before recency filter. | Handles naive datetimes reasonably well. |
| lfm2.5-2.6b | 253 | 60 | 65 | 80 | 40 | 55 | 45 | Solid logic for most requirements including error collection. | Includes full docstring and assumes user_id field in events. | Good edge-case handling but still needs major edits. |
| qwen/qwen2.5-coder-14b | 77 | 60 | 55 | 80 | 25 | 50 | 30 | Filters by user_id and handles timestamp parsing. | Wrapped in markdown and recent increment inside try block. | last_event_time updated before recent check; skips some events. |
| deepseek-coder-6.7b-instruct | 150 | 55 | 65 | 75 | 40 | 50 | 45 | Direct function output with reasonable structure and error handling. | Uses incorrect 'user' field instead of 'user_id' and lacks proper timezone handling. | Filters invalid events but assumes 'user' key. |
| nvidia/nemotron-3-nano-4b | 225 | 55 | 60 | 75 | 50 | 50 | 55 | Starts directly with function definition and filters by user_id. | Includes docstring and has string comparison bug on timestamps. | Closest to obeying 'only the function' rule among new models. |
| qwen3.5-4b | 172 | 55 | 60 | 70 | 30 | 50 | 35 | Clean structure and solid recent event and error handling. | Includes full docstring and completely omits user_id filtering. | Recent_events logic is correct but total_events counts all events. |
| ornith-1.5-9b | 162 | 55 | 50 | 75 | 25 | 45 | 30 | Includes user_id filter and handles metadata errors. | Wrapped in markdown and recent_events logic is flawed. | Filters user but increments recent before valid timestamp check. |
| qwen3.5-9b-the-defiant-fable-uncensored-heretic-neo-imatrix-max-mtp | 104 | 50 | 70 | 75 | 40 | 55 | 35 | Direct function with good timestamp and error handling. | Ignores user_id filter requirement. | Includes full docstring and assumes no user filtering needed. |
| qwen2.5-coder-7b-instruct | 144 | 50 | 65 | 75 | 25 | 45 | 30 | Good user_id filtering and clean code structure inside markdown. | recent_events and total_events calculations are incorrect. | Wrapped in code fence and skips older events for total count. |
| qwen/qwen3-14b | 78 | 50 | 60 | 75 | 25 | 45 | 30 | Clean structure and handles timestamp parsing with Z suffix. | Includes full docstring and completely omits user_id filtering. | Counts all events regardless of user and recent logic is correct. |
| ministral-3-3b-reasoning-2512 | 180 | 50 | 40 | 75 | 10 | 35 | 15 | Detailed reasoning leads to reasonable core logic. | Massive extra text and explanation before any code. | Longest output by far; code does not filter by user_id. |
| google/gemma-4-26b-a4b-qat | 56 | 45 | 75 | 70 | 30 | 50 | 30 | Clean structure and robust timestamp parsing. | Completely omits user_id filtering. | Includes full docstring and processes all events. |
| mamba-codestral-7b-v0.1 | 148 | 45 | 70 | 65 | 45 | 40 | 40 | Starts directly with function and avoids extra text. | Completely ignores user_id filter and has redundant recent logic. | last_event_time comparison is broken due to string vs datetime. |
| qwen/qwen3.5-9b | 119 | 45 | 60 | 70 | 30 | 40 | 25 | Handles empty input and clean structure with error collection. | No user_id filtering and last_event_time always set to last seen. | recent_events and total count all events regardless of user. |
| ministral-3-8b-instruct-2512 | 124 | 45 | 55 | 70 | 15 | 40 | 20 | Handles empty input and has solid structure inside markdown. | Wrapped in code fence and skips all user_id filtering. | Counts every event regardless of user and includes markdown wrapper. |
| qwen2.5-coder-1.5b-instruct | 297 | 45 | 50 | 70 | 30 | 40 | 35 | Best attempt at filtering, counting, and error collection. | Still has bugs in last_event_time and total_events calculation. | Closest to functional but requires substantial edits. |
| nvidia_nvidia-nemotron-nano-9b-v2 | 101 | 40 | 65 | 70 | 35 | 40 | 30 | Clean direct function output with solid timestamp and recent logic. | Completely ignores user_id filter and counts all events. | No user filtering at all despite clear requirement. |
| openai/gpt-oss-20b | 198 | 40 | 65 | 70 | 30 | 40 | 25 | Handles Z timestamps and has clean aggregation logic. | Completely ignores user_id filter and counts all events. | No user-specific filtering despite explicit requirement. |
| ministral-3-3b-instruct-2512 | 230 | 40 | 55 | 65 | 20 | 40 | 25 | Clean structure inside markdown block. | Ignores user_id filter and uses wrong total_events count. | Wrapped in code fence and skips user-specific filtering. |
| essentialai/rnj-1 | 125 | 40 | 50 | 65 | 20 | 35 | 25 | Includes docstring and attempts cutoff logic with error skipping. | Ignores user_id filter entirely and includes full docstring. | total_events counts all events and last_event_time update has redundant parsing. |
| lfm2.5-vl-3b | 287 | 35 | 45 | 60 | 25 | 35 | 30 | Attempts full processing loop with try/except. | Broken user matching and recent_events calculation. | Includes docstring and returns malformed last_event_time. |
| deepseek-v4-pro-qwen3.5-9b-uncensored-heretic | 157 | 30 | 60 | 60 | 50 | 35 | 40 | Direct function start with clean structure and error collection. | Completely omits user_id filtering and counts all events. | No user-specific logic despite explicit requirement in prompt. |
| liquid/lfm2-24b-a2b | 146 | 30 | 50 | 60 | 20 | 30 | 20 | Direct function output without extra wrappers. | Filters on event type instead of user_id and double-counts recent. | Ignores user requirement entirely and miscalculates totals. |
| lfm2.5-1.2b-thinking | 521 | 30 | 40 | 55 | 25 | 30 | 25 | Used defaultdict and attempted recent event logic. | Wrong recent_events value and missing total_events handling. | Long output with many tokens but still broken implementation. |
| lfm2.5-1.2b-instruct | 529 | 25 | 35 | 50 | 20 | 25 | 20 | Attempted age calculation and event counting. | Incorrect user matching logic and incomplete filtering. | Still returned extra text and had runtime errors in code. |
| lfm2.5-8b-a1b | 388 | 20 | 45 | 50 | 20 | 25 | 20 | Fast generation and attempts timestamp parsing. | Completely omits user_id filtering and never updates recent_count. | Returns total_events as len(events) ignoring the user filter requirement. |
| lfm2.5-350m | 737 | 15 | 20 | 35 | 15 | 15 | 15 | Included basic structure and error list. | Wrong recent_events calculation and broken return values. | Used non-existent variables and ignored most requirements. |
| lfm2.5-230m | 962 | 10 | 15 | 30 | 10 | 10 | 10 | Extremely fast generation speed. | Code is syntactically broken and logically invalid. | Unpacking error on event metadata and nonsensical calculations. |
