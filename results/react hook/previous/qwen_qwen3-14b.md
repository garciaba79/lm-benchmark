# Qwen Qwen3 14B
Model: qwen_qwen3-14b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

To track the **previous value** of a given prop or state in React using only built-in hooks and TypeScript, we can create a custom hook called `usePrevious`. This hook is designed to return the previous value from the last render, which is particularly useful for comparing values between renders (e.g., detecting changes in props or state).

---

### ✅ Key Features

- **Generic Type Support**: Works with any type (`T`) including primitives, objects, arrays, etc.
- **Initial Render Handling**: Returns `undefined` on the first render since there's no previous value yet.
- **No External Dependencies**: Uses only built-in React hooks like `useRef`.
- **Efficient and Lightweight**: Does not cause unnecessary re-renders or side effects.

---

### 🧠 Implementation Details

We use a `ref` to persist the last known value of the input across renders. On each render, we:

1. Capture the current value stored in the ref (this is the previous value).
2. Update the ref with the new current value.
3. Return the previously captured value.

This ensures that on every render, the hook returns the **previous** value from the last render cycle.

---

### 🧪 Example Usage

```tsx
import React, { useState } from 'react';
import usePrevious from './usePrevious';

const MyComponent = () => {
  const [count, setCount] = useState(0);
  const previousCount = usePrevious(count);

  return (
    <div>
      Current: {count}, Previous: {previousCount}
    </div>
  );
};
```

---

### 📦 Final Code

```tsx
import { useRef } from 'react';

/**
 * A custom hook that returns the previous value of a given generic type `T`
 * from the last render.
 *
 * @param value - The current value to track.
 * @returns The previous value, or `undefined` on the first render.
 */
const usePrevious = <T,>(value: T): T | undefined => {
  const ref = useRef<T | undefined>();

  // Capture the previous value before updating the ref
  const previousValue = ref.current;

  // Update the ref with the current value for the next render
  ref.current = value;

  return previousValue;
};

export default usePrevious;
```

---

### 📌 Notes

- This hook is **not** affected by React's rendering optimizations like `useMemo` or `useCallback`.
- It works well in both functional and class components (though it’s best used with functional components).
- The returned value will be `undefined` on the first render, which is expected behavior.

---

### ✅ Summary

This implementation of `usePrevious` provides a clean and efficient way to access previous values across renders using only React's built-in hooks. It ensures compatibility with any type and handles initial state correctly without requiring external libraries or complex logic.

10 t/s, 2902 tokens, 292s, 36%
