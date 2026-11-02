# Nemotron 3 Nano 4B
Model: nvidia/nemotron-3-nano-4b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Below is a **stand‑alone** implementation of `usePrevious` that works for any generic type `T`.  

* It uses only the built‑in React 18+ hooks (`useEffect`, `useRef`).  
* No external libraries are required.  
* The hook returns the value *from the previous render*. On the very first render it returns `undefined` (so you can safely compare/guard against it).  

```tsx
import { useEffect, useRef } from 'react';

/**
 * Returns the previous value of a generic component argument.
 *
 * @param value – the current value we want to remember as “previous”
 * @returns the value from the last render, or `undefined` on the first render
 */
function usePrevious<T>(value: T): T | undefined {
  // The ref is initialised with `undefined`. After the first effect run it holds
  // whatever was passed in on the previous frame.
  const prev = useRef<T>(undefined);

  useEffect(() => {
    // When the new value arrives, store it as “previous” for the next render.
    prev.current = value;
  }, [value]);   // ← runs after the first render

  return prev.current; // will be `undefined` on the very first render
}

/* ------------------------------------------------------------------ */
/* Example usage ------------------------------------------------------ */

function Counter() {
  const count = useState<number>(0);
  const previousCount = usePrevious(count);

  if (previousCount === undefined) {
    console.log('First render – no previous value');
  } else {
    console.log(`Prev: ${previousCount}, Current: ${count}`);
  }

  return <button onClick={() => setCount(c => c + 1)}>+</button>;
}
```

### Why this works

| Step | What happens |
|------|--------------|
| **Component mounts** | `usePrevious` creates a ref that starts with `undefined`. The effect runs once (with the initial `value`) and stores it as the “previous” value. On this first render `prev.current` is still `undefined`, which matches our contract. |
| **First render finishes** | After the effect resolves, `prev.current` holds the *old* value (`0`). |
| **User clicks** → state updates | New value (e.g., `1`) triggers the effect again: it overwrites `prev.current` with `1`. The component now receives that new value. |
| **Next render** | `usePrevious(count)` returns the previous value stored in the ref, i.e. `0`. |

### Return type

The hook is generic (`<T>`) and its return type is `T \| undefined`. This mirrors React’s typical “previous‑state” pattern (e.g., Redux’s `prevState`).

Feel free to drop this snippet into any TypeScript/JSX project that uses React 18+. No extra dependencies, no magic. 🚀

208 t/s, 979 tokens, 5s, 6%
