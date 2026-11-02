# LFM2.5 VL 3B
Model: lfm2.5-vl-3b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is the implementation for `usePrevious`.

This hook uses the `useRef` API to store the previous value. This ensures that the state persists across re-renders even if the component does not re-mount (which happens in many modern React patterns like `useEffect` or conditional rendering).

```typescript
import { useRef, useState } from 'react';

/**
 * Custom hook to access the previous value of a generic type T.
 * 
 * @param initialValue - The initial value to be stored as the previous state.
 * @returns The current value and a reference to the previous value.
 */
export function usePrevious<T>(initialValue: T): [T, React.RefObject<T>] {
  // Use ref to persist state across renders
  const prevValue = useRef<T>(initialValue);

  return [
    prevValue.current, // Return the current value for consumption
    prevValue,       // Return a reference to the previous value
  ];
}
```

### How it works:
1.  **`useRef<T>`**: This creates a mutable reference that persists across renders.
2.  **Initialization**: We pass `initialValue` into the ref's constructor. If this is the first render, the hook returns `[initialValue, null]`.
3.  **Return Value**: The function returns an array containing both the current value and the reference to the previous one.

### Usage Example:

```typescript
import React from 'react';
import { usePrevious } from './usePrevious';

const MyComponent = () => {
  // Initial state is set when the component mounts
  const [count, setCount] = usePrevious<number>(0);

  return (
    <div>
      <p>Current Count: {count}</p>
      
      // Update count on every render
      setCount(count + 1);
    </div>
  );
};

export default MyComponent;
```

263 t/s, 402 tokens, 2s, 3%
