# Falcon H1R 7B
Model: falcon-h1r-7b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Below is a **stand‑alone TypeScript hook** that works with React 18+ only (no external libraries).  
It stores the value from the previous render in a `ref`. On every render it returns the
value that was stored *after* the previous render, and returns `undefined` on the first mount.

```tsx
// usePrevious.ts
import React from "react";

/**
 * Returns the value of `current` from the last time a different value was rendered.
 * On the initial render it returns undefined because there is no previous value yet.
 *
 * The hook works for any type `T`.
 */
export function usePrevious<T>(current: T): T | undefined {
  // Keep the last value that was passed in. We start with undefined so that on mount we get undefined back.
  const previousRef = React.useRef<T | undefined>(undefined);

  /**
   * Run after every render (or only when dependencies change).  
   * If the stored value is not equal to the current one, replace it.
   * This ensures that on the next render we return the value from this render.
   */
  React.useEffect(() => {
    // Only update the reference when a new value appears.
    if (previousRef.current !== current) {
      previousRef.current = current;
    }

    // Cleanup is not needed because we only hold a ref, but we declare it for completeness.
    // In React 18+ the cleanup function will be called when unmounting or when deps change.
    return () => {
      // No mutable state to clean up → noop.
      void 0;
    };
  }, [current]);

  // Return what was stored after the previous render.
  // The cast is safe because the hook returns a union type that can be either T or undefined.
  return previousRef.current as T | undefined;
}
```

### How it works

1. **`previousRef`** keeps the value from the last render where a change was detected.  
   It starts with `undefined`, so on the very first mount the hook returns `undefined`.

2. The effect runs after every rendering pass (or only when `current` changes).  
   If the stored value is different, it gets overwritten with the new one.  

3. Because the effect executes **after** the return statement of the hook,
   `previousRef.current` still holds the value from the previous render, which we then return.

### Usage example

```tsx
import React, { useState } from "react";
import { usePrevious } from "./usePrevious";

function Counter() {
  // some state that changes over time
  const [count, setCount] = useState(0);

  // The hook returns undefined on the first render, then the previous count.
  const prevCount = usePrevious(count);

  return (
    <div style={{ padding: "1rem", fontFamily: "sans-serif" }}>
      {"counter: "}
      {count}
      <br />
      {"previous count: "}
      {prevCount ?? "N/A"}
      <br />
      <button onClick={() => setCount(c => c + Math.random() * 2)}>
        Increment randomly (+1 or +2)
      </button>
    </div>
  );
}

export default Counter;
```

Each time the button is pressed you’ll see:

- The current count after the increment.
- The value that was shown on the previous render (or “N/A” before any changes).

### Using with objects or arrays

```tsx
function ObjDemo() {
  const [obj, setObj] = useState({ name: "Alice", age: 30 });

  const prevObj = usePrevious(obj);

  // console.log(prevObj) → undefined on first render, then the previous object reference after each change.
}
```

Because we compare with strict equality (`!==`), a completely new object instance will always be treated as a change – exactly what most UI‑driven scenarios expect. If you need deep comparison, replace the check with an implementation that uses libraries like lodash or write your own.

### Edge Cases

* **First render:** returns `undefined`.  
  This is safe for any type because we declare the return as a union (`T | undefined`).  

* **Non‑primitive types (functions, class instances):** works unchanged; only reference equality matters.  

* **React 18+ concurrency mode:** The hook does not hold mutable state beyond the ref, so it won’t cause infinite loops or deadlocks in concurrent rendering.

---

#### TL;DR

```tsx
import { usePrevious } from "./usePrevious";

const prevValue = usePrevious(someGenericValue); // undefined on first render
```

That’s all you need—a tiny, generic hook that behaves exactly like the classic “previous‑render” pattern but typed safely for any TypeScript codebase. Happy coding! 🚀

95 t/s, 4810 tokens, 51s, 30%
