# LFM2.5 1.2B Thinking
Model: lfm2.5-1.2b-thinking
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```typescript
import { useRef } from 'react';

const usePrevious<T>(initialValue?: T): any = (prevRef: useRef<T | undefined>) => {
  return prevRef.current || initialValue;
};

// Usage example:
function MyComponent() {
  const previousValue = usePrevious<number>(0);
  console.log(previousValue); // Initial render returns undefined or provided initial value
}
```

**Explanation:**  
- The `usePrevious` hook uses a closure with a `useRef<T | undefined>` to store the last known value (`prevRef.current`).  
- On each render, it checks if `prevRef.current` exists (i.e., hasn't been set yet), returning `initialValue` or `undefined` if not initialized.  
- This ensures correct handling of initial renders by leveraging React's ref system and closure persistence within the hook's scope.

511 t/s, 3555 tokens, 7s, 22%
