# Gemma 4 12B
Model: google/gemma-4-12b
Test: Hook Previous
Created: 11/03/2026, 01:01:57 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

To implement this in React, we need to use `useRef` and `useEffect`. 

The key logic is that `useRef` stores a value that persists across renders, but we must update that ref **after** the render cycle (inside `useEffect`) so that it reflects the "previous" value during the *current* render.

Here is the production-ready implementation:

```typescript
import { useEffect, useRef } from 'react';

/**
 * A hook that returns the value of a prop/state from the previous render.
 * 
 * @param value - The value to track.
 * @returns The value from the previous render. On the initial render, it returns undefined (or the current value if you prefer logic adjustment).
 */
export function usePrevious<T>(value: T): T | undefined {
  // Use a ref to store the "current" value for the next render cycle
  const prevValueRef = useRef<T>(value);

  // Update the ref after every render. 
  // Because useEffect runs after the component is committed, 
  // when the component re-renders, 'prevValueRef.current' will still hold 
  // the value from the previous render until this effect finishes.
  useEffect(() => {
    prevValueRef.current = value;
  }, [value]);

  // Return the value that was set in the previous render cycle
  return prevValueRef.current;
}
```

### How to use it:

```tsx
import React, { useState } from 'react';
import { usePrevious } from './hooks/usePrevious';

const Counter = () => {
  const [count, setCount] = useState(0);
  
  // This will be 0 on the first render (since it's the initial value)
  // and will stay one step behind the 'count' state.
  const prevCount = usePrevious(count);

  return (
    <div>
      <h1>Current: {count}</h1>
      <h2>Previous: {prevCount === undefined ? 'None' : prevCount}</h2>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
};
```

### Key Technical Details:
1.  **Generic Type `<T>`**: This ensures type safety. If you pass a string, the return type is `string | undefined`; if you pass a number, it's `number | undefined`.
2.  **Complexity**: $O(1)$ time and space complexity.
3.  **Initial Render Behavior**: On the very first render, `prevValueRef.current` is initialized with the current value, but because the `useEffect` hasn't run yet, it effectively behaves as "initial" state. If you strictly need it to be `undefined` on the first render even if a value exists, you would initialize the ref with `undefined`.
4.  **Why `useEffect`?**: We use `useEffect` because React's rendering cycle follows a specific order: **Render -> Commit -> Effect**. By updating the Ref in the Effect phase, we ensure that during the Render phase, the Ref always holds the data from the *previous* completed render.

82 t/s, 695 tokens, 9s
