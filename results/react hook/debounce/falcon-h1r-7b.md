# Falcon H1R 7B
Model: falcon-h1r-7b
Test: Hook Debounce
Created: 11/02/2026, 06:22:56 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook useDebounce(value: any, delay: number) in TypeScript that returns a debounced version of the input value. It should update only after the specified delay has passed since the last change. Include proper cleanup on unmount.

Use React 18+, functional components, and avoid external libraries. Explain the benefits, pros, cons and any potential issues.

> #### 🤖 Assistant

## ✅ Debounced Hook in TypeScript  

Below is a self‑contained `useDebounce` hook that works with any React 18+ functional component, needs no external library and returns the latest input **only after the requested delay has elapsed**.  
It also cleans up pending timers when the component unmounts.

```tsx
import { useEffect, useRef, useState } from "react";

/**
 * Debounce hook
 *
 * Returns a value that updates only after `delay` ms have passed since the last change.
 * The returned type matches the incoming `value`.
 *
 * @param value   The current input (updates when this prop changes)
 * @param delay   Minimum time to wait before emitting a new value. Defaults to 300 ms.
 */
export function useDebounce<T>(value: T, delay?: number): T {
  // Normalise the delay – negative or zero means “no debouncing”.
  const normalizedDelay = Math.max(delay ?? 300, 0);

  /**
   * `latestValueRef` holds the most recent raw input so that we can:
   *   • Compare against previous value to avoid unnecessary timer creation.
   *   • Keep a stable reference for cleanup when the component unmounts.
   */
  const latestValueRef = useRef<T | null>(null);

  // State that holds the debounced output. Using an arrow‑function for the setter
  // prevents React from re‑rendering on every render call inside the effect.
  const [debounced, setDebounced] = useState<T>(() => undefined)[1];

  /** Timeout ID that is stored in a ref so it can be cleared later. */
  const timerIdRef = useRef<number>(-1);

  // ────── CLEAN‑UP ON UNMOUNT ───────────────────────────────────────────────
  useEffect(() => {
    return function cleanup() {
      if (timerIdRef.current !== -1) clearTimeout(timerIdRef.current);
    };
  }, []);

  // ────── RESPOND TO PROP CHANGES ───────────────────────────────────────────
  useEffect(() => {
    const previousRaw = latestValueRef.current;

    // Skip scheduling if the same value arrived again quickly.
    if (normalizedDelay > 0 && value === previousRaw) return;

    // Store current raw input so that a later change can compare against it.
    latestValueRef.current = value;

    // Cancel any pending timeout – we only want the most recent debounced value.
    clearTimeout(timerIdRef.current);

    // If delay is zero, update immediately without waiting for a timer.
    if (!normalizedDelay) {
      setDebounced(value);
      // No new timer created → keep timerIdRef at its old value.
      return;
    }

    const newTimerId = setTimeout(() => setDebounced(value), normalizedDelay);
    timerIdRef.current = newTimerId;

    /** Cleanup for this effect: if the input changes again before the timeout fires, clear it. */
    return function cancel() {
      clearTimeout(newTimerId);
    };
  }, [value]);

  // The hook returns whatever the debounced state currently holds.
  // If you need a fallback for the very first render you could initialise `debounced`
  // with a default value or copy from `latestValueRef` here.
  return debounced as T;
}
```

### How it works  

| Step | What happens | Why it matters |
|------|--------------|----------------|
| **1️⃣ Prop change → useEffect** | Whenever the incoming `value` prop changes, we store it in `latestValueRef`, cancel any old timeout and schedule a new one. | Guarantees that only the most recent value is ever emitted after delay. |
| **2️⃣ Timer fires → setDebounced** | After `delay` ms the callback runs and updates the debounce state with the latest input. | The component’s UI sees a new value only once the user has paused typing for at least `delay`. |
| **3️⃣ Unmount cleanup** | When the component is removed, we clear any pending timer to avoid stray timers that could keep JavaScript objects alive. | Prevents memory leaks in long‑living apps or hot‑reloading scenarios. |

---  

## 📦 Usage Example  

```tsx
import React, { useState } from "react";
import { useDebounce } from "./useDebounce";

export const SearchBox: React.FC<{ onSuggestions?: (data: string[]) => void }> = ({
  onSuggestions,
}) => {
  const [query, setQuery] = useState("");

  // Debounced version of the query – only after 300 ms of inactivity.
  const debouncedQuery = useDebounce(query, 300);

  // Run the expensive lookup once per idle period.
  React.useEffect(() => {
    if (!onSuggestions) return;
    // Imagine a costly async fetch:
    // onSuggestions([]).then((data) => setResults(data));
    onSuggestions(debouncedQuery);
  }, [debouncedQuery, onSuggestions]);

  return (
    <input
      type="text"
      value={query}
      placeholder="Search…"
      // Controlled component – parent updates the raw state.
      onChange={e => setQuery(e.target.value)}
    />
  );
};
```

---  

## ✅ Benefits of a Debounce Hook  

| Benefit | Explanation |
|---------|-------------|
| **Reduced UI churn** | Heavy operations (network calls, expensive calculations, DOM updates) are not triggered on every keystroke. The component renders only after the user pauses, resulting in smoother interactions. |
| **Lower CPU/Network load** | Prevents spamming APIs or performing costly computations many times per second. This is especially valuable for search suggestions, autocomplete, form validation, etc. |
| **Reusability** | A single generic hook can be dropped into any functional component without pulling in a library like lodash‑debounce. |
| **No external dependencies** | Uses only core React APIs (`useEffect`, `useState`, refs), keeping bundle size minimal and avoiding version conflicts. |

---  

## ⚠️ Cons & Potential Pitfalls  

| Issue | Why it matters / How to mitigate |
|-------|-----------------------------------|
| **Added latency** | The UI shows the result only after a short pause, which can feel like a lag for fast typists. Use a reasonable delay (e.g., 200‑300 ms) and let users know that suggestions appear when typing eases. |
| **Stale values on unmount** | If the component is destroyed before its timeout fires, the pending timer would otherwise keep an object alive. The hook’s cleanup clears it, but in long‑living trees you may still accumulate timers if components never truly unmount (e.g., infinite lists). Use keys and memoisation to avoid recreating hooks for identical elements. |
| **Race conditions with rapid changes** | When the input updates many times within a single animation frame, we cancel previous timers each time → only the last value wins. This matches typical debounce semantics but may be surprising if you expected intermediate values. If you need to emit *all* distinct recent values you’d have to implement an alternative strategy (e.g., requestAnimationFrame based queue). |
| **Zero/negative delay edge case** | The hook treats zero or negative delays as “no debounce” and updates immediately, but it still schedules a new timer each change if the delay is set later. Guard against unnecessary timers by comparing with previous value (already done) or simply return the raw prop when delay ≤ 0. |
| **Precision limits of `setTimeout`** | Timers are millisecond‑granular and subject to browser scheduling quirks. For sub‑millisecond delays you’d need a different approach (`performance.now`, `requestAnimationFrame`). The hook is designed for typical UI‑level debouncing where ms granularity is fine. |
| **Side‑effects in the callback** | The timer only calls `setDebounced`; never invoke async work directly inside that callback, otherwise you could end up with multiple concurrent timers. Usually you keep heavy work outside (e.g., `useEffect` after debounce fires). |

---  

## 🛠️ Extending the Hook (Optional)  

If you need more control you can augment the hook:

```tsx
export interface UseDebounceOptions<T> {
  /** Custom update function that receives the latest value. */
  onUpdate?: (value: T) => void;
}
```

Then expose a method to cancel/reset manually, support leading/trailing debouncing, or use `requestAnimationFrame`. But for most UI cases the simple version above is sufficient and easy to reason about.

---  

## 🎉 TL;DR  

*Use this generic `useDebounce<T>` hook whenever you need to throttle a value until the user stops interacting with it.*  
It gives you clean cleanup, works with any prop type, and avoids pulling in external libraries—perfect for React 18+ projects. Happy coding!

94 t/s, 6793 tokens, 72s, 42%
