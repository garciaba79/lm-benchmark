# GPT-OSS 20B
Model: openai/gpt-oss-20b
Test: Hook Debounce
Created: 11/02/2026, 06:22:56 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook useDebounce(value: any, delay: number) in TypeScript that returns a debounced version of the input value. It should update only after the specified delay has passed since the last change. Include proper cleanup on unmount.

Use React 18+, functional components, and avoid external libraries. Explain the benefits, pros, cons and any potential issues.

> #### 🤖 Assistant

## The Hook

```tsx
// useDebounce.tsx
import { useState, useEffect } from "react";

/**
 * Returns a debounced version of the supplied value.
 *
 * @template T - The type of `value`. It can be anything that you want to debounce.
 * @param value   – The current value you are watching for changes.
 * @param delayMs – Number of milliseconds to wait after the last change
 *                  before updating the returned value.
 * @returns {T} The debounced value, which only updates once `delayMs` has passed
 *              since the last change in `value`.
 *
 * @example
 * const [search, setSearch] = useState("");
 * const debouncedSearch = useDebounce(search, 300);
 *
 * // Inside an effect you can safely fire a request when debouncedSearch changes.
 */
export function useDebounce<T>(value: T, delayMs: number): T {
  // Keep a state that will hold the debounced value
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    // If `delayMs` is zero we can skip the timer entirely.
    if (delayMs <= 0) {
      setDebouncedValue(value);
      return;
    }

    // Set a timeout that updates the debounced value after `delayMs`.
    const handler = window.setTimeout(() => {
      setDebouncedValue(value);
    }, delayMs);

    // Cleanup: clear the timeout if either
    // 1) the component unmounts, or
    // 2) `value`/`delayMs` changes before the timeout fires.
    return () => {
      window.clearTimeout(handler);
    };
  }, [value, delayMs]); // Only re‑run when value or delay changes

  return debouncedValue;
}
```

> **Why `window.setTimeout`?**  
> In a browser environment that is the only global API we need.  
> If you ever run this in Node (e.g., server‑side rendering), you can replace it with `global.setTimeout`.

---

## How to Use It

```tsx
import { useState, useEffect } from "react";
import { useDebounce } from "./useDebounce";

export function SearchInput() {
  const [query, setQuery] = useState("");
  // Only updates after the user stops typing for 400 ms.
  const debouncedQuery = useDebounce(query, 400);

  useEffect(() => {
    if (!debouncedQuery) return;
    // Fire your API call here – it will only run once per pause in typing
    fetch(`/api/search?q=${encodeURIComponent(debouncedQuery)}`);
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

---

## Benefits

| Feature | Why it matters |
|---------|----------------|
| **Zero‑dependency** | No extra bundle weight or polyfills. |
| **TypeScript generics** | Works with any value type – string, number, object, etc. |
| **Cleanup on unmount** | The timeout is cleared when the component unmounts, preventing state updates after unmount (no memory leaks). |
| **Simple API** | `useDebounce(value, delay)` returns the debounced value; no extra callbacks or manual timers needed. |
| **Re‑usability** | Can be dropped into any functional component that needs a debounced value. |

---

## Pros & Cons

| Pros | Cons |
|------|------|
| **Performance** – Reduces expensive operations (API calls, re‑renders) to once per delay interval. | **Latency** – The consumer must tolerate the intentional delay; UI feels less immediate. |
| **Predictable** – Timeout is always cleared on value change or unmount. | **State duplication** – Two state variables (`value` & `debouncedValue`) exist; for very large objects you may want to debounce a function instead of data. |
| **Easy to reason about** – Pure effect with no side‑effects beyond the timer. | **No cancelable promise** – If you need to abort an in‑flight request when a new value arrives, you’ll have to add that logic separately (e.g., using `AbortController`). |

---

## Potential Issues & Edge Cases

1. **Zero or Negative Delay**  
   The hook treats non‑positive delays as “no debounce” and updates immediately. This avoids an unnecessary timer.

2. **Changing the Delay Dynamically**  
   If you change `delayMs` while a timeout is pending, the effect will clean up the old timeout and start a new one with the updated delay.

3. **Large Objects or Functions**  
   Debouncing objects can lead to stale references if the object is mutated elsewhere. Prefer immutable updates or debounce the *function* that handles the value instead.

4. **Server‑Side Rendering (SSR)**  
   `window` is undefined on the server, so this hook will crash if used during SSR. Wrap it in a check (`typeof window !== "undefined"`) or provide a no‑op fallback.

5. **Memory Leaks**  
   The cleanup function guarantees that timers are cleared, preventing leaks even if the component unmounts while waiting for the debounce delay.

---

## Summary

`useDebounce<T>(value, delay)` is a lightweight, type‑safe React hook that returns a debounced copy of any value. It updates only after `delayMs` milliseconds have passed without another change, cleans up timers on unmount or when inputs change, and introduces no external dependencies. Use it whenever you need to throttle expensive operations (API calls, filtering large lists, etc.) in response to rapid user input or rapidly changing props.

105 t/s, 1252 tokens, 13s, 9%
