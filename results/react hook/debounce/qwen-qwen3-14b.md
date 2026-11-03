# Qwen3 14B
Model: qwen/qwen3-14b
Test: Hook Debounce
Created: 11/03/2026, 01:10:35 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook useDebounce(value: any, delay: number) in TypeScript that returns a debounced version of the input value. It should update only after the specified delay has passed since the last change. Include proper cleanup on unmount.

Use React 18+, functional components, and avoid external libraries. Explain the benefits, pros, cons and any potential issues.

> #### 🤖 Assistant

Here's a complete implementation of the `useDebounce` custom React hook using **React 18+**, **TypeScript**, and **functional components** — without relying on any external libraries like `lodash`.

---

### ✅ **useDebounce Hook Implementation in TypeScript**

```tsx
import { useState, useEffect, useRef } from 'react';

// Custom debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  const timeoutRef = useRef<number | null>(null);

  useEffect(() => {
    // Clear previous timeout if it exists
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Set new timeout for debouncing
    timeoutRef.current = window.setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cleanup function: clear timeout on unmount or value change
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [value, delay]);

  return debouncedValue;
}
```

---

### 🧠 **Explanation of the Code**

- **`useState<T>`**: Used to store and update the debounced value.
- **`useRef<number | null>`**: Stores a reference to the `setTimeout` ID for cleanup.
- **`useEffect`**:
  - Triggers on changes in `value` or `delay`.
  - Clears any existing timeout before setting up a new one.
  - Sets a new timer that updates the state after `delay` milliseconds.
  - Returns a cleanup function that clears the timer when the component unmounts or re-renders.

---

### 🎯 **Benefits of Using Debounce**

- **Improves performance**: Reduces frequent calls to expensive functions like API requests, search lookups, etc.
- **Enhances user experience**: Prevents janky UI updates and unnecessary rendering caused by rapid input changes (e.g., typing in a search field).
- **Reduces server load**: Minimizes the number of API calls made during user interaction.

---

### ⚖️ **Pros vs Cons**

| **Pros** | **Cons** |
|----------|-----------|
| Reduces unnecessary updates and API calls | Slightly delays the response, which may affect real-time interactions |
| Easy to integrate with React hooks and functional components | Requires careful handling of cleanup to avoid memory leaks or lingering timeouts |
| Works well for search fields, input validation, etc. | May not be suitable for use cases where immediate feedback is essential |

---

### 🔒 **Potential Issues & How to Avoid Them**

1. **Incorrect Cleanup**:
   - If `useEffect` doesn't clean up the timeout properly on unmount or value change, it can lead to memory leaks.
   - ✅ Solved by returning a cleanup function from `useEffect`.

2. **Stale Closures in Timeout Callbacks**:
   - If not handled carefully, timeouts may reference outdated values of `value`.
   - ✅ Not an issue here because we're using the latest value via `useState` and re-creating the timeout on every render.

3. **Unexpected Behavior with Complex Values (Objects/Arrays)**:
   - If you're debouncing complex values like objects or arrays, ensure your equality check is correct.
   - ✅ In our case, `useState<T>` handles this automatically as it's shallowly compared.

4. **Using in Effects**:
   - Be cautious when using `useDebounce` inside `useEffect` — use the debounced value only if needed and properly handle cleanup.
   - ✅ Our implementation is safe for such use cases.

---

### 📌 **Usage Example**

```tsx
import React, { useState } from 'react';
import { useDebounce } from './useDebounce';

const SearchComponent: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const debouncedInput = useDebounce(inputValue, 500);

  useEffect(() => {
    console.log('Searching with:', debouncedInput);
    // Perform search or API call here
  }, [debouncedInput]);

  return (
    <div>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Search..."
      />
    </div>
  );
};
```

---

### 🧪 **Testing the Hook**

- Simulate rapid input changes.
- Ensure that the debounced value updates only after the delay has passed.
- Confirm that no timers are left hanging after unmounting.

---

If you're looking to extend this hook further (e.g., for more advanced use cases like throttling or custom equality checks), it's also possible — but for most common use cases, `useDebounce` as shown above is sufficient.

79 t/s, 1024 tokens, 13s
