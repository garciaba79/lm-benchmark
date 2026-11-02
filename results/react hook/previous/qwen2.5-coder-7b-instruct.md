# Qwen2.5 Coder 7B Instruct
Model: qwen2.5-coder-7b-instruct
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Certainly! Below is an implementation of the `usePrevious` hook in TypeScript using React 18+ hooks:

```typescript
import { useRef } from 'react';

function usePrevious<T>(value: T): T | undefined {
    const ref = useRef<T>();

    // Store current value in ref on every render
    useEffect(() => {
        ref.current = value;
    }, [value]);

    // Return previous value stored in ref, or undefined if it's the initial render
    return ref.current;
}

export default usePrevious;
```

### Explanation:

1. **useRef**: We create a mutable `ref` object that will store the previous value of the input.
2. **useEffect**: This hook is used to update the `ref.current` with the current value whenever it changes. The dependency array `[value]` ensures that this effect runs every time `value` changes.
3. **Return Value**: We return `ref.current`, which will be the previous value from the last render or `undefined` if it's the initial render.

### Usage Example:

```typescript
import React, { useState } from 'react';
import usePrevious from './usePrevious';

const Counter: React.FC = () => {
    const [count, setCount] = useState(0);
    const previousCount = usePrevious(count);

    return (
        <div>
            <p>Current Count: {count}</p>
            <p>Previous Count: {previousCount !== undefined ? previousCount : 'Initial'}</p>
            <button onClick={() => setCount(prevCount => prevCount + 1)}>Increment</button>
        </div>
    );
};

export default Counter;
```

In this example, `usePrevious` is used to track the previous value of `count`. When you click the "Increment" button, it updates the state and displays both the current and previous counts. On the initial render, `previousCount` will be `undefined`.

This implementation ensures that the hook works correctly with any type and handles initial renders appropriately.

137 t/s, 420 tokens, 3s, 3%
