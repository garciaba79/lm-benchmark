# Qwen3 14B
Model: qwen/qwen3-14b
Test: Hook Previous
Created: 11/03/2026, 01:11:02 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's how you can write a custom React hook called `usePrevious` in **TypeScript** that works with **React 18+**, using only built-in hooks:

---

### ✅ `usePrevious` Hook in TypeScript (React 18+)

```tsx
import { useRef, useEffect } from 'react';

/**
 * A custom hook that returns the previous value of a generic type T.
 * @param value - The current value to track.
 * @returns The previous value from the last render.
 */
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}
```

---

### 📌 How It Works

- `useRef` is used to store the previous value in a mutable reference that persists across renders.
- `useEffect` runs after every render and updates the ref with the current value.
- On **initial render**, `ref.current` is initially `undefined`, which represents "no previous value".
- From the second render onward, it returns the value from the previous render.

---

### 🧪 Example Usage

```tsx
import React, { useState } from 'react';
import { usePrevious } from './usePrevious';

const Counter: React.FC = () => {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>Current Count: {count}</p>
      <p>Previous Count: {prevCount ?? 'N/A'}</p>
      <button onClick={() => setCount(prev => prev + 1)}>Increment</button>
    </div>
  );
};
```

---

### 🔍 Notes

- The hook returns `undefined` on the **first render**, since there's no previous value.
- You can safely use this with any type: numbers, strings, objects, arrays, etc.
- It works well with complex values like objects or arrays (because it stores a reference to them).

---

Let me know if you want a version that returns `null` instead of `undefined` on initial render!

80 t/s, 455 tokens, 6s
