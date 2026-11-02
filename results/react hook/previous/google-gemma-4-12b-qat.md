# Gemma 4 12B QAT
Model: google/gemma-4-12b-qat
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

To implement a `usePrevious` hook in React 18+, we need to use `useState` and `useEffect`. Since React's state updates are asynchronous, we must store the current value in a state variable during the render phase and "sync" it to a ref or a state that reflects the value from the *previous* render.

Here is the production-ready implementation:

```typescript
import { useEffect, useRef } to any } from 'react';

/**
 * A custom hook that returns the previous value of a prop, state, 
 * or any other value from the previous render.
 * 
 * @param value - The current value to track.
 * @returns The value from the previous render. On the initial render, returns undefined.
 */
function usePrevious<T>(value: T): T | undefined {
  // We use a ref to store the value because updating a ref 
  // does not trigger a re-render.
  const ref = useRef<T>(value);

  // We use useEffect to update the ref after the render is committed.
  // This ensures that 'ref.current' always holds the value from the previous render.
  useEffect(() => {
    ref.current = value;
  }, [value]);

  // Return the value stored in the ref.
  return ref.current;
}

export default usePrevious;
```

### How it works:
1.  **The Ref**: We initialize a `useRef` with the current `value`. Because `useRef` persists its content between renders but doesn't trigger a re-render when changed, it is the perfect storage for "history."
2.  **The Effect**: The `useEffect` hook runs *after* the component has finished rendering and the DOM has been updated. By updating `ref.current` inside the effect, we ensure that the value inside the ref is only updated *after* the user sees the current render.
3.  **The Return**: When the component renders, it returns `ref.current`. On the first render, it returns the initial value. On every subsequent render, it returns what the value was during the *previous* render.

### Usage Example:

```tsx
import React, { useState } from 'react';
import usePrevious from './usePrevious';

const Counter = () => {
  const [count, setCount] = useState<number>(0);
  
  // This will always be one step behind 'count'
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>Current: {count}</p>
      <p>Previous: {prevCount}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
};
```

### Key Technical Details:
*   **Generic Type `<T>`**: This ensures full type safety. If you pass a string, it returns `string | undefined`. If you pass an object, it returns `Object | undefined`.
*   **Initial Render**: On the very first mount, `prevCount` will be `undefined` (or the initial value depending on how you initialize the ref), which is the standard behavior for this hook.
*   **Complexity**: This is $O(1)$ time and space complexity.

94 t/s, 714 tokens, 8s, 5%
