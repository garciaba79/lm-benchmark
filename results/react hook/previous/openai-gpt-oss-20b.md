# GPT-OSS 20B
Model: openai/gpt-oss-20b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here’s a tiny, type‑safe `usePrevious` hook you can drop into any React 18+ project:

```tsx
// usePrevious.ts
import { useEffect, useRef } from 'react';

/**
 * Returns the value that was passed to this hook on the previous render.
 *
 * @template T The type of the value you’re tracking. It can be anything – primitives,
 * objects, arrays, functions… just pass it through and the hook will preserve the
 * exact same reference.
 *
 * @param {T} value The current value that should become “previous” after this render.
 *
 * @returns {T | undefined}
 *   - On the very first render `undefined` is returned (no previous value exists).
 *   - From the second render onward, it returns the value that was supplied on
 *     the previous invocation of the component.
 */
export function usePrevious<T>(value: T): T | undefined {
  // Persist a ref across renders – this is where we’ll store the "previous" value.
  const ref = useRef<T>();

  // After every render, update the ref with the current value so that it will be
  // available to the next invocation of the hook.
  useEffect(() => {
    ref.current = value;
  }, [value]);

  // On this render we can safely read the previous value from the ref.
  return ref.current;
}
```

### How it works

| Step | What happens |
|------|--------------|
| **First render** | `ref.current` is initially `undefined`. The hook returns that. After the effect runs, `ref.current` becomes the current value. |
| **Subsequent renders** | The hook reads `ref.current`, which now holds the *previous* value, and returns it. Then the effect updates the ref with the new value for the next cycle. |

Because we’re only using `useRef` (which survives across renders) and a plain `useEffect`, there are no external dependencies or performance pitfalls.

### Usage example

```tsx
import { useState } from 'react';
import { usePrevious } from './usePrevious';

function Counter() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>Current: {count}</p>
      <p>Previous: {prevCount ?? 'none yet'}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
}
```

### Why this pattern is safe

* **Type safety** – The generic `T` ensures that the hook’s return type matches whatever you pass in.
* **No stale closures** – By updating the ref inside a `useEffect`, we guarantee that the latest value is stored *after* React has committed the render, preventing race conditions.
* **Zero external deps** – Only built‑in React hooks are used; no third‑party libraries or context.

Feel free to copy this into your project and start tracking previous values in any component!

133 t/s, 725 tokens, 6s, 5%
