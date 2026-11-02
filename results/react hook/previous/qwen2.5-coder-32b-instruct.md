# Qwen2.5 Coder 32B Instruct
Model: qwen2.5-coder-32b-instruct
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Certainly! Below is an implementation of a custom React hook called `usePrevious` in TypeScript that takes a value of generic type `T` and returns the previous value from the last render. This hook handles initial renders correctly by returning `undefined` on the first render.

```typescript
import { useEffect, useRef } from 'react';

function usePrevious<T>(value: T): T | undefined {
  // Create a ref to store the previous value
  const prevValueRef = useRef<T>();

  // Update the ref with the current value after rendering
  useEffect(() => {
    prevValueRef.current = value;
  }, [value]);

  // Return the previous value from the ref
  return prevValueRef.current;
}

export default usePrevious;
```

### Explanation:
1. **Generic Type `T`**: The hook is generic, meaning it can accept any type of value.
2. **useRef**: A `ref` is used to store the previous value. Since a `ref` holds its state across renders and doesn't trigger re-renders when updated, it's perfect for this use case.
3. **useEffect**: The `useEffect` hook updates the `prevValueRef.current` with the current value of `value` after every render. This ensures that on the next render, the previous value is available.
4. **Return Value**: On the first render, `prevValueRef.current` will be `undefined`. After subsequent renders, it will hold the value from the last render.

### Usage Example:
Here's an example of how you might use the `usePrevious` hook in a component:

```typescript
import React, { useState } from 'react';
import usePrevious from './usePrevious';

function Counter() {
  const [count, setCount] = useState<number>(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>Current count: {count}</p>
      <p>Previous count: {prevCount !== undefined ? prevCount : 'N/A'}</p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  );
}

export default Counter;
```

In this example, the `Counter` component uses the `usePrevious` hook to keep track of the previous count value and displays it alongside the current count. On the initial render, the previous count will show "N/A" because `prevCount` is `undefined`.

6 t/s, 513 tokens, 91s, 4%
