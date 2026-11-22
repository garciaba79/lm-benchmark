# Gemma 4 26B A4B QAT
Model: google/gemma-4-26b-a4b-qat
Test: Hook Previous
Created: 11/22/2026, 03:09:14 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

To implement a `usePrevious` hook in React, we leverage the `useRef` hook. Since `useRef` persists its value across renders but updating a ref does not trigger a re-render, we can use a `useEffect` to update the ref *after* the component has rendered with the current value.

Here is the robust TypeScript implementation.

```typescript
import { useRef, useEffect } from 'react';

/**
 * A custom hook that returns the previous value of a passed-in value.
 * 
 * @param value - The current value that you want to track.
 * @returns The value from the previous render.
 * 
 * @template T - The type of the value being tracked.
 */
function usePrevious<T>(value: T): T | undefined {
  // We use a ref to store the value from the previous render.
  // We initialize it as undefined because on the first render, 
  // there is no "previous" value.
  const ref = useRef<T>();

  // useEffect runs AFTER the render is committed to the screen.
  // This means when 'value' changes, the component re-renders,
  // the hook returns the 'old' value stored in the ref,
  // and then we update the ref to the 'new' value for the next render.
  useEffect(() => {
    ref.current = value;
  }, [value]);

  // Return the value currently held in the ref (which is the value from the PREVIOUS render).
  return ref.current;
}

export default usePrevious;
```

### How it works (Step-by-Step)

1.  **Initial Render:**
    *   `value` is `A`.
    *   `useRef` initializes `ref.current` as `undefined`.
    *   The hook returns `undefined`.
    *   `useEffect` runs (after render) and sets `ref.current = A`.
2.  **Second Render (Value changes to `B`):**
    *   `value` is `B`.
    *   The hook returns `ref.current`, which is currently `A`.
    *   `useEffect` runs (after render) and sets `ref.current = B`.
3.  **Third Render (Value changes to `C`):**
    *   `value` is `C`.
    *   The hook returns `ref.current`, which is currently `B`.
    *   `useEffect` runs and sets `ref.current = C`.

### Usage Example

```tsx
import React, { useState } from 'react';
import usePrevious from './usePrevious';

const Counter: React.FC = () => {
  const [count, setCount] = useState<number>(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <h1>Current: {count}</h1>
      <h2>Previous: {prevCount ?? 'None'}</h2>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
};
```

### Key Technical Details:
*   **Generics (`<T>`)**: By using a generic type, the hook maintains strict type safety. If you pass a `number`, the return type is `number | undefined`.
*   **Strict Mode Compatibility**: This pattern is compatible with React 18's Strict Mode. While `useEffect` might run twice in development, the logic remains sound because the ref update only happens after the commit phase.
*   **Complexity**: Time complexity is $O(1)$ and Space complexity is $O(1)$.

57 t/s, 793 tokens, 14s, 5%
