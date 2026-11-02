# Qwen2.5 Coder 14B
Model: qwen/qwen2.5-coder-14b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

To create a `usePrevious` custom hook in TypeScript that works with React 18+, you can use the `useRef` hook to store the previous value. Here's how you can implement it:

```typescript
import { useRef, useEffect } from 'react';

function usePrevious<T>(value: T): T | undefined {
    const ref = useRef<T>();

    // Store current value in ref after component is rendered
    useEffect(() => {
        ref.current = value;
    }, [value]); // Only re-run the effect if value changes

    // Return previous value (happens before update in useEffect above)
    return ref.current;
}

export default usePrevious;
```

### Explanation:
- **`useRef<T>()`:** This initializes a mutable reference object. The `.current` property of the returned object will be updated with the new value every render.
- **`useEffect(() => { ... }, [value])`:** This effect runs after each render. It updates the `ref.current` to the current value, ensuring that the previous value is stored before the component re-renders.
- **Return Value:** The hook returns the `ref.current`, which holds the previous value from the last render.

### Usage Example:

Here's an example of how you can use the `usePrevious` hook in a functional component:

```typescript
import React, { useState } from 'react';
import usePrevious from './usePrevious';

const Counter: React.FC = () => {
    const [count, setCount] = useState(0);
    const previousCount = usePrevious(count);

    return (
        <div>
            <p>Current Count: {count}</p>
            <p>Previous Count: {previousCount !== undefined ? previousCount : 'N/A'}</p>
            <button onClick={() => setCount(prevCount => prevCount + 1)}>Increment</button>
        </div>
    );
};

export default Counter;
```

In this example, the `Counter` component uses the `usePrevious` hook to display both the current and previous count values. When the button is clicked, the count increments, and the previous value is displayed correctly.

This implementation ensures that the `usePrevious` hook works correctly even during the initial render by returning `undefined` for the first time (since there's no previous value).

78 t/s, 482 tokens, 6s, 3%
