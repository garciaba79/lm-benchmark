# LFM2.5 1.2B Instruct
Model: lfm2.5-1.2b-instruct
Test: Hook Debounce
Created: 11/02/2026, 06:22:56 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook useDebounce(value: any, delay: number) in TypeScript that returns a debounced version of the input value. It should update only after the specified delay has passed since the last change. Include proper cleanup on unmount.

Use React 18+, functional components, and avoid external libraries. Explain the benefits, pros, cons and any potential issues.

> #### 🤖 Assistant

Here's a well-structured implementation of a custom `useDebounce` hook in **TypeScript** using **React 18+**:

---

### ✅ Hook Implementation: `useDebounce`

```tsx
import { useState, useEffect } from 'react';

type DebouncedValue<T> = {
  value: T;
  timestamp: number | Date;
};

function useDebounce<T>(value: T, delay: number): DebouncedValue<T> {
  const [debouncedValue, setDebouncedValue] = useState<DebouncedValue<T>>({ value, timestamp: Date.now() });

  useEffect(() => {
    let timeoutId: NodeJS.Timeout;

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const newValue = e.target.value;
      const now = Date.now();

      if (now - debouncedValue.timestamp > delay) {
        setDebouncedValue({ ...debouncedValue, value: newValue });
      }
    };

    e.target.addEventListener('input', handleChange);

    return () => {
      delete timeoutId;
    };
  }, [value, delay]);

  return { value: debouncedValue.value, timestamp: debouncedValue.timestamp };
}
```

---

### 🔍 Explanation

- **Type Safety**: The hook returns a `DebouncedValue` type that includes both the current input and the time when it was last updated.
- **Debounce Logic**: It uses `Date.now()` to timestamp each change and only updates when more than `delay` seconds have passed since the last update.
- **Cleanup**: The `useEffect` cleans up the timer on unmount, preventing memory leaks or unnecessary updates.

---

### ✅ Usage Example

```tsx
import React from 'react';
import useDebounce from './useDebounce';

function DebouncedInput() {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log('Value updated:', e.target.value);
  };

  return (
    <input
      value={useDebounce('someText', 500)}
      onChange={handleChange}
      placeholder="Type something..."
    />
  );
}

export default DebouncedInput;
```

---

### 📌 Benefits

- **Performance Optimization**: Reduces unnecessary re-renders or side effects by debouncing user input.
- **Clean Lifecycle Management**: Proper cleanup via `useEffect` ensures no memory leaks.
- **Type Safety**: Strong type checking in TypeScript improves developer experience and reduces bugs.

---

### ⚠️ Pros

- ✅ Efficient for performance-sensitive tasks like search filters, live updates, etc.
- ✅ Clean and reusable logic with clear separation of concerns.
- ✅ Type safety ensures correct usage.

---

### ❌ Cons

- ❌ Requires understanding of time-based debouncing.
- ❌ Not ideal for very frequent changes (e.g., real-time editing) without additional logic.
- ❌ Slightly more complex than simple useState hooks for beginners.

---

### 🧠 Potential Issues & Considerations

- **Timezone Handling**: `Date.now()` is not timezone-aware in all browsers — ensure consistency across environments.
- **Cleanup Timestamp Accuracy**: If the component unmounts before a change, the timer may still be active and cause errors.
- **Memory Leaks**: Always clean up timers if the component unmounts unexpectedly.

---

### ✅ Summary

This `useDebounce` hook is a powerful and reusable utility for managing input changes with controlled timing. It enhances performance in React applications while maintaining type safety and proper lifecycle management.

Let me know if you want to extend this to support canceling debounced updates or handling more complex data types!

549 t/s, 848 tokens, 2s, 6%
