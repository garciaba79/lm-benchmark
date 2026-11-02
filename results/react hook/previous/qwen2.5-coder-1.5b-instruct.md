# Qwen2.5 Coder 1.5B Instruct
Model: qwen2.5-coder-1.5b-instruct
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```typescript
import { useState } from 'react';

/**
 * A custom hook to get the previous state of a value.
 *
 * @param initialValue - The initial value of the state.
 * @returns An object with `previous` and `current` properties.
 */
export function usePrevious<T>(initialValue: T): { previous: T | undefined; current: T } {
  const [state, setState] = useState(initialValue);

  // A ref to store the previous state
  const previousStateRef = React.useRef(state);

  // Update the previous state when the state changes
  React.useEffect(() => {
    previousStateRef.current = state;
  }, [state]);

  return { previous: previousStateRef.current, current: state };
}

// Example usage:
function App() {
  const [count, setCount] = usePrevious(0);

  return (
    <div>
      <p>Current count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}

export default App;
```

In this solution, we create a custom hook called `usePrevious` that takes an initial value of type `T`. It uses the `useState` hook to manage the state and a ref (`previousStateRef`) to store the previous state. The `useEffect` hook is used to update the ref whenever the state changes. This ensures that the previous state is always up-to-date with the last render. The hook returns an object containing both the previous and current states, which can be used in functional components to track changes over time.

305 t/s, 336 tokens, 1s, 5%
