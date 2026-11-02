# LFM2.5 2.6B
Model: lfm2.5-2.6b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is the implementation of the `usePrevious` hook in TypeScript using React 18+ hooks (`useRef`). This approach avoids unnecessary re-renders and handles the initial render state correctly by returning `undefined` (or the first value if provided) before updating the reference for subsequent renders.

```typescript
import { useRef } from 'react';

/**
 * A custom hook that returns the previous value of a given state variable.
 * 
 * @template T - The type of the value being tracked.
 * @param current - The current value to track. This will be set as the "previous" value on the next render.
 * @returns The previous value from the last render, or undefined if it's the first render.
 */
export function usePrevious<T>(current: T): T {
  // Use a ref to store the previous value. Refs persist across renders without causing re-renders themselves.
  const prev = useRef<T>();

  // If this is the very first render, `prev.current` will be undefined (default state of useRef).
  // We return it immediately to satisfy the function signature and handle "initial" correctly.
  // On subsequent renders, we update `prev` with the current value so it becomes available as the previous one next time.

  prev.current = current;

  // Return the stored previous value (which was from the last render).
  return prev.current;
}
```

### How it works:

1. **`useRef<T>`**: We use a ref to store the "previous" state. Refs are mutable and persist across component re-renders without triggering new renders themselves, making them ideal for caching values between renders.
2. **First Render**: When the component mounts, `prev.current` is initially `undefined`. The hook returns `undefined`, indicating there was no previous value yet.
3. **Subsequent Renders**:
   - The function updates `prev.current = current`. This saves the current render's value for future use.
   - It then immediately returns `prev.current`, which now holds the value from the *previous* render.

### Example Usage:

```tsx
import { usePrevious } from './usePrevious';

function Counter() {
  const name = "Alice";
  
  // On first render, 'previously' is undefined.
  // On second render (after clicking), it returns "Alice".
  const previouslyUsedName = usePrevious<string>();

  return (
    <div>
      <p>The previous name was: {previouslyUsedName}</p>
    </div>
  );
}

export default Counter;
```

260 t/s, 4244 tokens, 16s, 26%
