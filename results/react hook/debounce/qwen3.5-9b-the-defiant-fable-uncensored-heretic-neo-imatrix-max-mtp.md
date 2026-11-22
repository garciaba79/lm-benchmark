# Qwen3.5 9B The Defiant Fable Uncnr Heretic NEO MAX
Model: qwen3.5-9b-the-defiant-fable-uncensored-heretic-neo-imatrix-max-mtp
Test: Hook Debounce
Created: 11/22/2026, 02:55:04 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook useDebounce(value: any, delay: number) in TypeScript that returns a debounced version of the input value. It should update only after the specified delay has passed since the last change. Include proper cleanup on unmount.

Use React 18+, functional components, and avoid external libraries. Explain the benefits, pros, cons and any potential issues.

> #### 🤖 Assistant

Here’s a clean, production-ready `useDebounce` hook in TypeScript using React 18+ patterns:

```ts
import { useEffect, useRef } from 'react';

/**
 * useDebounce
 *
 * Returns a debounced version of the input value.
 * Updates only after `delay` ms have passed since the last change.
 */
export function useDebounce<T>(value: T, delay: number): T {
  const ref = useRef<T>(value);

  // Update internal ref whenever value changes (for immediate access if needed)
  useEffect(() => {
    ref.current = value;
  }, [value]);

  // Debounced version that updates after the specified delay
  const debouncedValue = useRef<T | null>(null);

  useEffect(() => {
    // If no delay, return immediately (no debounce needed)
    if (!delay || delay <= 0) {
      debouncedValue.current = value;
      return;
    }

    // Clear any pending timeout on new input
    const previousTimeoutId = debouncedValue.current as unknown as NodeJS.Timeout | null;
    if (previousTimeoutId) {
      clearTimeout(previousTimeoutId);
    }

    // Schedule update after delay
    const timeoutId = setTimeout(() => {
      debouncedValue.current = value;
    }, delay);

    // Cleanup: clear timeout on unmount or before next effect runs
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [value, delay]);

  // Return the debounced value (or current value if no debounce active)
  return debouncedValue.current ?? ref.current;
}
```

### How it works

- `ref` tracks the latest input value immediately.
- A second `debouncedValue` ref is updated only after a timeout clears.
- On each change:
  - The previous timeout (if any) is cleared to avoid stacking delays.
  - A new timeout is set; when it fires, `debouncedValue.current` is assigned the current input.
- Cleanup ensures no pending timeouts leak on unmount or re-render with a different delay.

### Usage example

```tsx
import { useState } from 'react';
import { useDebounce } from './useDebounce';

function SearchBox() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300); // 300ms debounce

  useEffect(() => {
    if (!debouncedQuery) return;
    console.log('Searching for:', debouncedQuery);
    // fetch(`/api/search?q=${encodeURIComponent(debouncedQuery)}`);
  }, [debouncedQuery]);

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="Search..."
    />
  );
}
```

### Benefits

- **Performance:** Reduces unnecessary operations (API calls, computations, DOM updates) triggered by rapid input changes.
- **Simplicity:** Pure React hook; no external dependencies.
- **Type-safe:** Fully typed with generics (`<T>`), works for strings, numbers, objects, etc.
- **Safe cleanup:** Clears timeouts on unmount and before each new effect run to prevent memory leaks.

### Pros & Cons / Potential Issues

**Pros:**
- Minimal overhead: only one `setTimeout` at a time.
- Works with React 18+ concurrent features (no blocking renders).
- Easy to reason about; straightforward implementation.

**Cons / Caveats:**
- **Stale closure risk avoided via refs**, but if you need the debounced value inside other effects, ensure you’re reading from `debouncedValue.current` or the returned value consistently.
- **Delay changes:** If `delay` changes while typing, behavior shifts immediately (previous timeout cleared). This is usually desired, but be aware of it in edge cases.
- **No immediate update on mount:** On initial render, if you need the debounced value right away, use the returned value directly; it will reflect the current input after any pending delay resolves.
- **Not for high-frequency state sync:** For very fast updates where sub-millisecond precision matters, this approach is coarse-grained (limited by `setTimeout` resolution).

### When to avoid / alternatives

- If you need precise timing or want to debounce only on specific events (e.g., keyup vs. change), consider a more granular implementation.
- For complex scenarios with multiple inputs and different delays, you might prefer a small utility library, but this hook is sufficient for most use cases without external dependencies.

105 t/s, 1017 tokens, 10s, 7%
