# Ornith 1.5 9B
Model: ornith-1.5-9b
Test: Hook Debounce
Created: 11/02/2026, 06:22:56 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook useDebounce(value: any, delay: number) in TypeScript that returns a debounced version of the input value. It should update only after the specified delay has passed since the last change. Include proper cleanup on unmount.

Use React 18+, functional components, and avoid external libraries. Explain the benefits, pros, cons and any potential issues.

> #### 🤖 Assistant

# useDebounce Hook in TypeScript

## Implementation

```typescript
import { useState, useEffect } from 'react';

/**
 * Returns a debounced version of `value`. The returned value only updates
 * after `delay` milliseconds have elapsed since the last change to `value`.
 */
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    // Schedule an update of debouncedValue after `delay` ms.
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cleanup: cancel the pending timer whenever value/delay change or on unmount.
    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}
```

## Usage Example

```tsx
import { useState, useEffect } from 'react';
import { useDebounce } from './useDebounce';

function SearchBox() {
  const [query, setQuery] = useState('');
  // Only re-fetch after the user stops typing for 300ms.
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery) {
      console.log('Searching for:', debouncedQuery);
      fetchResults(debouncedQuery); // your API call here
    }
  }, [debouncedQuery]);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

## How It Works

1. `useState` holds the latest debounced value, initialized to the initial input.
2. On every render where `value` or `delay` changes, the effect:
   - Cancels any previously scheduled timer (via cleanup).
   - Schedules a new `setTimeout` that calls `setDebouncedValue(value)` after `delay` ms.
3. Because React runs the **cleanup before** re-running the effect when dependencies change, each new keystroke cancels the previous pending update and starts a fresh countdown. Only once changes stop for `delay` ms does the final value propagate to state (triggering one render).

## Benefits

- **Zero dependencies** — no need for `lodash.debounce` or similar libraries.
- **Type-safe** — the generic `<T>` preserves the input type, so callers get full inference (`debouncedQuery: string`).
- **Self-contained & testable** — easy to drop into any component and reason about.

## Pros & Cons

| Aspect | Details |
|--------|---------|
| ✅ Correct trailing-edge debounce | Final value appears only after changes pause for `delay` ms. |
| ✅ Proper cleanup on unmount | Prevents timers firing after the component is gone (avoids React warnings / stale state updates). |
| ✅ Handles rapid changes | Each change resets the timer, so bursts collapse into a single update. |
| ⚠️ Extra render per value change | The effect runs and schedules a timer on every `value` change; negligible for typical input but not free. |
| ⚠️ Not leading-edge aware | It only fires *after* changes stop — you can't react to the first keystroke immediately without extra logic. |
| ⚠️ No timing metadata | Doesn't tell you *when* the last change happened (unlike timestamp-based variants). |

## Potential Issues & Edge Cases

1. **Stale closures** — The `value` captured inside `setTimeout` is safe here because `value` is a dependency and cleanup cancels stale timers before re-running. This is the key correctness guarantee; omitting it would cause bugs.

2. **Missing cleanup → memory leak / errors** — If you forget `clearTimeout`, timers keep running after unmount, firing `setState` on an unmounted component (React logs a warning and wastes work). Always return the cleanup function.

3. **`delay = 0`** — Technically works but effectively updates on the next tick; it's not really useful as a debounce in that case.

4. **Rapid non-user changes** — If `value` is updated very fast (e.g., during animations or high-frequency polling), debouncing may delay responses unexpectedly. Usually desired for input, but worth considering your use case.

5. **Initial render timing** — On mount the effect schedules a timer that sets `debouncedValue` to the same initial value; React bails out of re-rendering since nothing changed. Harmless.

## Alternative: Timestamp-Based Version

If you need finer control (e.g., knowing *when* the last change occurred, or implementing leading-edge behavior), track timestamps in a ref instead of relying solely on effect cleanup:

```typescript
import { useState, useEffect, useRef } from 'react';

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  const lastChangeRef = useRef<number | null>(null);

  useEffect(() => {
    if (lastChangeRef.current !== null) {
      clearTimeout(lastChangeRef.current);
    }

    lastChangeRef.current = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      if (lastChangeRef.current !== null) {
        clearTimeout(lastChangeRef.current);
      }
    };
  }, [value, delay]);

  return debouncedValue;
}
```

For the common case of debouncing search input or form fields, the first version is cleaner and idiomatic. Reach for the ref-based variant only when you need extra behavior beyond a simple trailing-edge debounce.

131 t/s, 4006 tokens, 31s, 25%
