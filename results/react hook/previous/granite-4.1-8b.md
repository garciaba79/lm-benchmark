# Granite 4.1 8B
Model: granite-4.1-8b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Certainly! Below is a TypeScript implementation of a custom React hook named `usePrevious`. This hook captures the previous value of any generic type `T` across component renders. It leverages the `useState` and `useEffect` hooks from React to manage state efficiently, ensuring it works correctly even on initial renders.

```typescript
import { useState, useEffect, useRef } from 'react';

/**
 * Custom hook to get the previous value of a variable.
 * @param value The current value which may change over time.
 * @returns The previous value before the last render. Returns undefined for the first render.
 */
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);
  useEffect(() => {
    // Update the reference to the latest value at each render
    ref.current = value;
  }, [value]); // Re-run effect whenever `value` changes

  return ref.current; // Return the previous value stored in the reference
}

// Example usage within a functional component:
/*
function MyComponent() {
  const number = useState(0)[0];
  const prevNumber = usePrevious(number);

  return (
    <div>
      Current: {number}, Previous: {prevNumber}
    </div>
  );
}
*/
```

### Explanation:

1. **TypeScript Generics**: The hook uses TypeScript generics (`<T>`) to ensure it can handle any type of value, making it versatile for use with numbers, strings, objects, arrays, or custom types.

2. **`useRef` Hook**: A `useRef` hook is employed to create a mutable ref object (`ref`). This object's `.current` property is used to store the last rendered value of `value`. `useRef` is ideal for storing values that persist across renders without causing re-renders themselves.

3. **`useState` and `useEffect`**: Although not directly used in this hook (since we're only managing state within the hook), understanding their role is crucial:
   - `useState` would typically be used to manage local component state.
   - `useEffect` is used here to update the ref's `.current` value whenever `value` changes, ensuring that the ref always holds the previous value from the last render.

4. **Handling Initial Renders**: On the first render, `ref.current` defaults to `undefined`, which is appropriate since there is no "previous" value yet. Subsequent renders will update this reference appropriately.

5. **No External Libraries**: This implementation relies solely on React's built-in hooks, ensuring compatibility with React 18 and beyond without dependency on external libraries.

This hook can be seamlessly integrated into any functional component to access the previous value of a prop or state variable, facilitating animations, comparisons, or any logic that requires knowledge of prior states.

126 t/s, 581 tokens, 5s, 4%
