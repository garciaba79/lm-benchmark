# Qwen3.8 27B
Model: qwen/qwen3.8-27b
Test: Hook Debounce
Created: 11/03/2026, 02:22:28 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook useDebounce(value: any, delay: number) in TypeScript that returns a debounced version of the input value. It should update only after the specified delay has passed since the last change. Include proper cleanup on unmount.

Use React 18+, functional components, and avoid external libraries. Explain the benefits, pros, cons and any potential issues.

> #### 🤖 Assistant

```typescript
import { useEffect, useState } from 'react';

/**
 * Debounce a value so it only updates after a specified delay has passed
 * since the last change.
 *
 * @param value - The value to debounce
 * @param delay - The delay in milliseconds before the debounced value updates
 * @returns The debounced value
 */
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cleanup: clear the timeout if the value changes or the component unmounts
    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}

export default useDebounce;
```

## Explanation

### How It Works

1. **State Initialization**: The hook initializes a `debouncedValue` state with the current `value`.
2. **Effect Hook**: Whenever `value` or `delay` changes, the `useEffect` hook:
   - Sets a `setTimeout` for the specified `delay`.
   - When the timer fires, it updates `debouncedValue` to the latest `value`.
3. **Cleanup**: The cleanup function clears the pending `setTimeout` before the next effect runs (when `value` changes) or when the component unmounts. This ensures that stale updates are prevented and no timers are left running after unmount.

### Benefits

- **Reduced Rendering**: Prevents excessive re-renders caused by rapid changes (e.g., typing in an input field).
- **Simplicity**: No external dependencies; uses only core React hooks.
- **Correctness**: Proper cleanup ensures no memory leaks from uncleared timeouts.
- **Flexibility**: Works with any data type `T` thanks to generics.

### Pros

- **Pure React**: Built with `useState` and `useEffect`, no additional libraries.
- **Type-Safe**: Uses TypeScript generics for type safety.
- **Predictable Behavior**: The debounced value updates exactly once after the delay from the last change.
- **Clean Unmount**: Timers are properly cleared on unmount, preventing side effects.

### Cons

- **Initial Render**: On the first render, `debouncedValue` immediately reflects `value` (since no delay has elapsed yet). If you need the initial value to also be debounced, additional logic would be required.
- **Delay Sensitivity**: If `delay` is very large, the UI may feel laggy.
- **No Cancellation Control**: Once started, the debounce timer cannot be manually cancelled or reset externally.
- **Double Invocation in Strict Mode**: In React 18 Strict Mode, effects run twice in development. This is handled correctly (the cleanup runs between the two executions), but it may be confusing during debugging.

### Potential Issues

1. **Rapid Changes Reset the Timer**: Each change to `value` resets the timer. This is the expected behavior for debouncing, but if you need *throttling* (limiting execution frequency) instead, this hook is not suitable.
2. **Memory Leaks (Avoided)**: Without the cleanup function, `setTimeout` would fire after unmount, causing a "setState on unmounted component" warning. The cleanup prevents this.
3. **Value Comparison**: The hook uses referential equality for `value`. If `value` is an object or array, it will be considered "changed" on every render even if its contents are the same. For complex objects, ensure you pass a stable reference or use memoized values.
4. **Delay Change**: If `delay` changes, the timer is reset. This is generally fine but could be surprising if `delay` is dynamic.
5. **React 18 Strict Mode**: In development, effects are mounted, unmounted, and remounted. The cleanup handles this correctly, but it may appear as if the debounce is "reset" twice. This is a development-only behavior and does not affect production.

### Usage Example

```tsx
import { useState } from 'react';
import useDebounce from './useDebounce';

function SearchInput() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  // Use debouncedQuery for API calls
  useEffect(() => {
    if (debouncedQuery) {
      fetchResults(debouncedQuery);
    }
  }, [debouncedQuery]);

  return (
    <input
      type="text"
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="Search..."
    />
  );
}
```

In this example, the `fetchResults` call is only triggered after the user stops typing for 300ms, reducing unnecessary API calls.

17 t/s, 1080 tokens, 63s
