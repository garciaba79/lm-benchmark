# Ministral 3 3B Reasoning 2512
Model: ministral-3-3b-reasoning-2512
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 32K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's the final implementation of the `usePrevious` hook in TypeScript, which works for any type and handles initial renders correctly using React 18+ hooks without external libraries:

```typescript
import { useRef } from 'react';

function usePrevious<T>(currentValue: T): T | undefined {
  const prevRef = useRef<{ value: T; isFirstRender: boolean }>();
  if (!prevRef.current) {
    // First render, initialize and return undefined
    prevRef.current = { value: currentValue, isFirstRender: true };
    return undefined;
  }

  // Subsequent renders: save previous value and update ref to current
  const temp = prevRef.current.value; // This is of type T because it was set in the previous call
  prevRef.current.value = currentValue;
  return temp;
}
```

This implementation uses a `useRef` to store an object that contains both the previous value and a flag indicating whether it's the first render. On the first call, the ref is initialized with the current value and the flag set to true, and undefined is returned. On subsequent calls, the previous value is saved in a temporary variable, the ref is updated with the new current value, and the old value is returned.

The use of a ref ensures that the state does not cause unnecessary re-renders, and the type system in TypeScript guarantees that the function works correctly for any type `T`, including those that might include undefined. The hook is designed to work with React 18+ hooks and does not rely on external libraries.

172 t/s, 11257 tokens, 65s, 35%
