# Nvidia NVIDIA Nemotron Nano 9B v2
Model: nvidia_nvidia-nemotron-nano-9b-v2
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a well-structured and type-safe implementation of the `usePrevious` React hook in TypeScript, designed to work with any generic type `T` and handle initial renders correctly using only React 18+ hooks:

---

### ✅ **`usePrevious` Hook Implementation**

```tsx
import { useRef, useEffect } from 'react';

/**
 * A custom React hook that returns the previous value of a given value from the last render.
 * 
 * @param value - The current value to track (of any type).
 * @returns The previous value from the last render, or `null` on the first render.
 */
function usePrevious<T>(value: T): T | null {
  // Ref to store the previous value
  const prevRef = useRef<T>(null);

  // Update the ref with the current value when it changes
  useEffect(() => {
    prevRef.current = value;
  }, [value]);

  // Return the previous value (or null on first render)
  return prevRef.current;
}

export default usePrevious;
```

---

### 🧠 **How It Works**

- **`useRef<T>(null)`**: Creates a mutable reference to store the previous value. The type `T` ensures type safety.
- **`useEffect(() => { ... }, [value])`**: This effect runs whenever the `value` changes. It updates the ref with the current value, effectively capturing the "previous" value for the next render.
- **Return Value**:
  - On the **first render**, `prevRef.current` is `null`, so the hook returns `null`.
  - On subsequent renders, it returns the value that was passed in during the previous render.

---

### 🧪 **Example Usage**

```tsx
import React, { useState } from 'react';
import usePrevious from './usePrevious';

function Counter() {
  const [count, setCount] = useState(0);

  // Get the previous count value
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>Current Count: {count}</p>
      <p>Previous Count: {prevCount !== null ? prevCount : 'N/A'}</p>
      <button onClick={() => setCount(prevCount === null ? 1 : prevCount + 1)}>
        Increment
      </button>
    </div>
  );
}

export default Counter;
```

---

### 📌 **Key Features**

- ✅ **Type-safe**: Works with any type `T` (numbers, strings, objects, etc.).
- ✅ **Handles initial render**: Returns `null` on the first render.
- ✅ **No external dependencies**: Uses only React 18+ hooks (`useRef`, `useEffect`).
- ✅ **Efficient**: Only updates the ref when the value changes.

---

This implementation is clean, efficient, and adheres to React best practices. It's ideal for tracking previous values in components where you need to compare or log state changes.

102 t/s, 2479 tokens, 24s, 16%
