# LFM2.5 24B A2B
Model: lfm2.5-24b-a2b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

**Solution**

```tsx
import { useRef } from "react";

/**
 * Hook that returns the value of the previous render.
 *
 * - On the first call (the initial mount) no “previous” value exists,
 *   so `undefined` is returned and the supplied value is stored in a ref.
 * - On subsequent calls the hook returns the value that was rendered
 *   in the last render, then updates the ref with the current value.
 *
 * The hook works for any generic type T (primitives, objects, arrays …)
 * and uses only React’s built‑in hooks (React 18+).
 */
export function usePrevious<T>(value: T): T | undefined {
  // `prev` will hold the value from the previous render.
  const prevRef = useRef<T | undefined>(undefined);

  if (prevRef.current === undefined) {
    // First render – nothing has been rendered yet. Store this value
    // for the next time we need a “previous” one and return `undefined`.
    prevRef.current = value;
    return undefined as T | undefined;
  } else {
    // A previous value already exists → that’s exactly what the hook is supposed to return.
    const previousValue: T = prevRef.current; // type‑guaranteed by the guard above
    // Update the ref for the next render.
    prevRef.current = value;
    return previousValue;
  }
}
```

### How it works

1. **First render** – `prevRef.current` is still `undefined`.  
   The hook stores the supplied `value` in the reference and returns `undefined`, signalling that there is no earlier render yet.

2. **Subsequent renders** – `prevRef.current` now holds the value that was rendered in the previous pass of the component function. That exact object (`previousValue`) is returned, giving you the “old” value while the current `value` is saved back into the reference for future comparisons.

Because only a simple ref is used, the hook has **no dependencies on any external library** and works with React 18 (the API surface hasn’t changed since earlier versions).

### Example usage

```tsx
import { useState } from "react";
import { usePrevious } from "./usePrevious";

function Counter() {
  const [count, setCount] = useState<number>(0);
  const prevCount = usePrevious(count); // ← previous count value

  return (
    <div>
      <p>Current: {count}</p>
      <p>Previous: {prevCount ?? "—"}</p>

      <button onClick={() => setCount(c => c + 1)}>
        Increment
      </button>
    </div>
  );
}
```

- On the first render `prevCount` is `undefined`.
- After clicking **Increment** once (changing `count` from 0 to 1), `prevCount` becomes `0` – exactly the value that was rendered on the previous render.
- The pattern works identically for objects, arrays, or any other generic type.

105 t/s, 4961 tokens, 48s, 31%
