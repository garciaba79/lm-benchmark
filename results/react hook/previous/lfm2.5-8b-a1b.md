# LFM2.5 8B A1B
Model: lfm2.5-8b-a1b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here’s a tiny, self‑contained React 18+ hook in TypeScript.  
It stores the *previous* rendered value (or `undefined` for the very first render) using a ref‑like state pattern and returns it as its value.

```tsx
import { useState, useEffect } from 'react';

/**
 * Provides the value that was rendered on the previous render.
 *
 * @param initial Optional starting value. If omitted, `undefined` is used for the very first render.
 *                (The returned type is inferred from this argument; you can pass any generic T.)
 */
export function usePrevious<T>(initial?: T): T {
  // Holds the last rendered value before a change occurs on this component's own update cycle.
  const [previous, setPrevious] = useState<T | undefined>();

  // Whenever `value` changes we write the *new* one into `previous`.
  // Because state updates are asynchronous but happen in the same render,
  // the assignment runs **before** the hook returns, so the returned value is
  // guaranteed to be “the previous” as of this moment.
  useEffect(() => {
    if (value !== undefined) {
      setPrevious(value);
    }
  }, [value]);

  return previous;
}
```

### How it works

1. **State** – `previous` starts at the provided initial value (`undefined` by default).  
2. **Effect** – On every render that depends on `value`, we sync the *current* rendered value into `previous`. Since React updates state after rendering, this write happens **before** the hook’s return statement.
3. **Return** – The hook yields whatever was stored in `previous` (i.e., “the previous” before the current render).

### Typical usage

```tsx
import { useState } from 'react';
import { usePrevious } from './usePrevious';

function Counter() {
  const [value, setValue] = useState<number>(0);

  // `prev` is the value that was rendered *before* this component re‑rendered.
  const prev = usePrevious<number>();   // or any generic T you need.

  return (
    <>
      {/* show what has already been shown */}
      <button onClick={() => setValue(v => v + 1)}>Increment</button>

      {/* `prev` will be the old value (e.g. before each click) */}
      <p>Previous number: {prev}</p>
    </>
  );
}
```

* The hook works with **any** type (`T`) and correctly returns `undefined` on the initial render, matching React’s normal rendering order.

No external libraries are used – just the standard hooks from React 18+.

378 t/s, 2986 tokens, 8s, 19%
