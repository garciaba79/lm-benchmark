# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: Hook Previous
Created: 11/03/2026, 02:58:14 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```typescript
import { useRef, useEffect } from 'react';

function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

export default usePrevious;
```

This hook works by:

1. Creating a `useRef` to store the previous value
2. Using `useEffect` to update the ref with the current value after each render
3. Returning the stored previous value (which will be `undefined` on the first render)

The hook handles all types through TypeScript's generic system (`<T>`), and properly manages the initial render case where there was no previous value. The `useEffect` dependency array `[value]` ensures the ref is updated whenever the input value changes, but since we're using a ref (which persists between renders), it correctly captures the previous value for the next render cycle.

Usage example:
```typescript
const count = usePrevious(value); // Returns undefined on first render, then previous value
```

64 t/s, 225 tokens, 4s
