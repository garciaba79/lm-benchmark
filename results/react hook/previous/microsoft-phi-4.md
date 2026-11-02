# Phi 4
Model: microsoft/phi-4
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

To create a custom React hook called `usePrevious` using TypeScript, you can leverage the `useRef` and `useEffect` hooks provided by React. This hook will track the previous value of a given input across renders.

Here's how you can implement it:

```typescript
import { useRef, useEffect } from 'react';

function usePrevious<T>(value: T): T | undefined {
  // Use a ref to store the previous value
  const prevRef = useRef<T | undefined>();

  // Update the ref after every render with the current value
  useEffect(() => {
    prevRef.current = value;
  }, [value]); // Only re-run if the value changes

  // Return the stored previous value (initially, it will be `undefined`)
  return prevRef.current;
}

export default usePrevious;
```

### Explanation:

1. **Generics:** The hook is typed with a generic `<T>`, which allows it to handle any type of input.

2. **useRef Hook:** We use `useRef` to create a mutable object (`prevRef`) that persists across renders without causing additional renders itself.

3. **useEffect Hook:** After each render, we update the current value stored in `prevRef.current` with the new value passed into the hook. The dependency array `[value]` ensures this effect runs only when `value` changes.

4. **Return Value:** The function returns `prevRef.current`, which holds the previous value from the last render. On the initial render, it will return `undefined`.

This hook effectively captures and provides access to the previous value of any given input across component renders in a type-safe manner using TypeScript.

81 t/s, 345 tokens, 4s, 2%
