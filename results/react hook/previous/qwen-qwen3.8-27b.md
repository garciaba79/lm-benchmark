# Qwen3.8 27B
Model: qwen/qwen3.8-27b
Test: Hook Previous
Created: 11/03/2026, 02:24:45 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```typescript
import { useRef } from 'react';

/**
 * React hook that returns the previous value from the last render.
 * On the first render, it returns undefined (or the initial value if provided).
 * 
 * @param value - The current value to track
 * @returns The previous value from the last render (undefined on first render)
 */
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);
  
  // Use the previous pattern: store the current value in the ref after reading it
  // We need to capture the value before it changes, so we use the standard pattern
  // where we read the ref's current value (which holds the previous render's value)
  // and then update it.
  
  // Actually, the correct implementation:
  // - On first render, ref.current is undefined, so we return undefined
  // - On subsequent renders, ref.current holds the value from the previous render
  // - We then update ref.current to the current value
  
  const previous = ref.current;
  ref.current = value;
  
  return previous;
}
```

19 t/s, 253 tokens, 14s
