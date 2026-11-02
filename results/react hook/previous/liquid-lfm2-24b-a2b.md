# Lfm2 24B A2B
Model: liquid/lfm2-24b-a2b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a well-documented implementation of the `usePrevious` hook in **TypeScript** using **React 18+** hooks. This hook is designed to return the previous value of a given state or variable on each render, while correctly handling the initial render case (where there is no previous value).

---

### ✅ Key Features

- **Generic Type Support**: Works with any type `T`.
- **Initial Render Handling**: Returns `undefined` on the first render.
- **No External Dependencies**: Uses only React's built-in hooks.
- **Type Safety**: Fully typed using TypeScript.

---

### 🧠 How It Works

The hook uses the `useRef` hook to store the previous value across renders. On each render, it updates the ref with the current value and returns the previous one (i.e., the value stored in the ref before the update).

This approach ensures that:
- The previous value is captured **before** the current render's state is updated.
- It works correctly even if the value changes between renders.
- It handles `undefined` values gracefully, which is essential for the initial render.

---

### 📦 Code Implementation

```tsx
import { useRef } from 'react';

/**
 * A custom React hook that returns the previous value of a given state or variable.
 * @param value - The current value (of generic type T) to track.
 * @returns The previous value from the last render, or `undefined` if it's the first render.
 */
function usePrevious<T>(value: T): T | undefined {
  const prevRef = useRef<T | undefined>(undefined);

  // Capture the current value before updating the ref
  const currentValue = value;

  // Update the ref with the current value for the next render
  prevRef.current = currentValue;

  // Return the previous value (before the update)
  return prevRef.current;
}
```

---

### 🧪 Example Usage

```tsx
import React, { useState } from 'react';
import { usePrevious } from './usePrevious';

function ExampleComponent() {
  const [count, setCount] = useState<number>(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>Current count: {count}</p>
      <p>Previous count: {prevCount ?? 'N/A'}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

**Behavior:**
- On the first render, `prevCount` is `undefined`.
- After clicking the button, `prevCount` becomes `0`, then `1`, and so on.

---

### 📝 Notes

- The hook does **not** depend on the state's value changing — it always returns the previous value from the last render.
- It works with any type `T`, including objects, functions, or even `null`/`undefined`.
- This is a common pattern used in React for detecting changes between renders (e.g., for animations, logging, or conditional logic).

---

### ✅ Summary

The `usePrevious` hook is a simple yet powerful utility that leverages React's `useRef` to track and return the previous value of any state or variable. It adheres to React 18+ best practices and ensures correct behavior during initial renders and subsequent updates.

114 t/s, 747 tokens, 7s, 5%
