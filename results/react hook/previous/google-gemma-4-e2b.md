# Gemma 4 E2B
Model: google/gemma-4-e2b
Test: Hook Previous
Created: 11/15/2026, 09:43:53 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is the implementation of the `usePrevious` hook in TypeScript:

```tsx
import { useRef, useEffect } from 'react';

/**
 * A custom React hook that returns the previous value of a state or prop 
 * from the last render.
 *
 * @template T The type of the value being tracked.
 * @param {T} value The current value to track.
 * @returns {T | undefined} The previous value, or undefined if it's the initial render.
 */
export function usePrevious<T>(value: T): T | undefined {
  // useRef holds the value from the previous render. 
  // We initialize it with the current value.
  const ref = useRef<T>(value);

  // useEffect runs after every render, allowing us to update ref 
  // with the 'value' from the *just completed* render cycle.
  useEffect(() => {
    ref.current = value;
  }, [value]); // Dependency array ensures this runs whenever 'value' changes

  // Return the value stored in ref.current. 
  // It will be 'undefined' on the very first render because 'ref.current' is initialized with the first 'value'.
  return ref.current;
}

// --- Example Usage ---

interface CounterProps {
  initialCount: number;
}

/**
 * A component demonstrating the usePrevious hook.
 */
export function Counter(props: CounterProps) {
  // 1. Use usePrevious to get the previous count
  const prevCount = usePrevious(props.initialCount);

  // 2. Internal state for demonstration
  const [count, setCount] = React.useState(props.initialCount);

  const increment = () => {
    setCount(prev => prev + 1);
  };

  return (
    <div>
      <h2>usePrevious Example</h2>
      <p>Current Count: {count}</p>
      {/* prevCount will be undefined on the first render */}
      <p>Previous Count: {prevCount === undefined ? 'N/A (Initial Render)' : prevCount}</p>

      <button onClick={increment}>Increment</button>
    </div>
  );
}

// Example of how to use it in an application context (if needed for testing)
/*
import React from 'react';

function App() {
    const [count, setCount] = React.useState(0);
    
    // Use the hook on state changes
    const prevCount = usePrevious(count);

    return (
        <div>
            <h1>App State</h1>
            <p>Current: {count}</p>
            <p>Previous: {prevCount === undefined ? 'N/A' : prevCount}</p>
            <button onClick={() => setCount(c => c + 1)}>Increment</button>
        </div>
    );
}
*/
```

### Explanation:

1.  **Generic Type `<T>`**: The hook is generic, meaning it can track any type (numbers, strings, objects, etc.).
2.  **`useRef<T>(value)`**: We use `useRef` to store a mutable reference that persists across renders but whose changes do not trigger re-renders. This is the perfect place to store the "previous" value. It's initialized with the incoming `value`.
3.  **`useEffect(() => { ref.current = value; }, [value])`**: This effect runs after every render where `value` has changed. Inside it, we update `ref.current` to hold the `value` that was just passed into the component during that render cycle. By using `value` in the dependency array, we ensure the reference is updated whenever the input value changes.
4.  **Return `ref.current`**: The hook returns the current value stored in the ref.
    *   On the **first render**, `ref.current` holds the initial `value`.
    *   On subsequent renders (after the `useEffect` has run), `ref.current` holds the `value` from the *immediately preceding* render, achieving the desired "previous value" effect.

188 t/s, 905 tokens, 5s
