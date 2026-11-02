# LFM2.5 1.2B Instruct
Model: lfm2.5-1.2b-instruct
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Sure! Below is an example implementation of a custom React hook called `usePrevious` in TypeScript that works with generic types `T`. This hook maintains the previous value from the last render and can be used to access it during rendering.

```typescript
import { useRef } from 'react';

interface UsePrevious<T> {
  prevValue: T | undefined;
}

export function usePrevious<T>(initial: T): UsePrevious<T> {
  const prevValueRef = useRef<T | undefined>(undefined);
  
  // Initialize the hook with a value
  return () => ({
    prevValue: initial,
    prevValueRef
  });
}

// Example usage in a functional component:
const MyComponent = () => {
  const [prev, setPrev] = usePrevious<number>(0);

  let count = 0;

  const handleChange = () => {
    setCount(count + 1);
    prevValueRef.current = count;
  };

  return (
    <div>
      {count}
      <button onClick={handleChange}>Next</button>
    </div>
  );
};
```

### Explanation:
- **Type Safety:** The hook is generic (`<T>`) and ensures that `prevValue` can be either a value of type `T` or `undefined`.
- **Initial Render Handling:** When the component first renders, it initializes with the given initial value.
- **Persistence:** The previous value from the last render stays in memory because `useRef` retains its value across re-renders.
- **Usage Pattern:**
  - Call `usePrevious<number>(0)` to initialize with a starting number (e.g., 0).
  - Each time you update state, store that new value in `prevValueRef.current`.
  - Access the previous value using `prevValueRef.current`.

Would you like me to extend this hook so it can be used for managing time-based or other dynamic values?

524 t/s, 425 tokens, 1s, 3%
