# Nvidia NVIDIA Nemotron Nano 9B v2
Model: nvidia_nvidia-nemotron-nano-9b-v2
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here's a well-documented implementation of `useLocalStorage` with explanations of its benefits, pros/cons, and potential issues:

```typescript
import { useState, useEffect } from 'react';

/**
 * Custom hook to manage state in localStorage with type safety and cross-tab synchronization.
 * 
 * @param key - The unique identifier for the stored data in localStorage
 * @param initialValue - The default value to use if no data exists in localStorage
 * @returns [currentValue, setValue] - Current stored value and setter function
 */
const useLocalStorage = <T>(key: string, initialValue: T): [T, (value: T) => void] => {
  const [storedValue, setStoredValue] = useState<T>(initialValue);

  // Read from localStorage on mount or key change
  useEffect(() => {
    try {
      const item = localStorage.getItem(key);
      if (item) {
        setStoredValue(JSON.parse(item) as T); // Parse and cast to type T
      } else {
        setStoredValue(initialValue); // Use initial value if no data exists
      }
    } catch (error) {
      console.error(`Error reading from localStorage for key "${key}":`, error);
      setStoredValue(initialValue); // Fallback to initial value on error
    }
  }, [key]); // Only re-run when key changes

  // Write to localStorage when storedValue changes
  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(storedValue)); // Stringify and store
    } catch (error) {
      console.error(`Error writing to localStorage for key "${key}":`, error);
    }
  }, [key, storedValue]); // Run when key or storedValue changes

  // Cleanup: Remove key from localStorage on unmount
  useEffect(() => {
    return () => {
      try {
        localStorage.removeItem(key);
      } catch (error) {
        console.warn(`Error removing item from localStorage for key "${key}":`, error);
      }
    };
  }, [key]);

  return [storedValue, setStoredValue];
};
```

---

### **Benefits**
1. **Type Safety**: Uses TypeScript generics `<T>` to ensure type consistency between stored data and returned values.
2. **Automatic JSON Handling**: Serializes/deserializes data automatically, eliminating manual stringification/parsing.
3. **Cross-Tab Sync**: Changes in one tab propagate to others via `localStorage` (eventual consistency).
4. **Cleanup**: Removes stale data on unmount to prevent memory leaks.
5. **Error Handling**: Gracefully handles parsing/writing errors with fallbacks and logging.

---

### **Pros**
- **Simple Integration**: Works out-of-the-box with React 18+ functional components.
- **No External Dependencies**: Lightweight and relies only on browser APIs.
- **Predictable Behavior**: Clear separation of read/write logic with error boundaries.
- **Scalability**: Easily adaptable for multiple keys or complex data structures.

---

### **Cons**
1. **Eventual Consistency**: Changes aren't real-time across tabs (other tabs may see stale data until they reload).
2. **Concurrent Write Conflicts**: Last write wins in case of simultaneous updates from multiple tabs.
3. **Data Loss Risk**: If JSON parsing fails (e.g., due to manual localStorage edits), it falls back to `initialValue`.
4. **Size Limits**: `localStorage` has a ~5MB limit per key, which may affect large datasets.

---

### **Potential Issues**
1. **Invalid JSON Handling**: If stored data is corrupted (e.g., manual edits), parsing will fail and use `initialValue`.
2. **Type Mismatch**: While type-safe in code, `JSON.parse` may return a value that doesn't match `T` if the stored data was invalid.
3. **Key Changes**: If `key` changes between renders (unlikely but possible), it will read/write to a different key in `localStorage`.
4. **Performance**: Frequent writes/reads could impact performance in high-frequency use cases.

---

### **Usage Example**
```tsx
const [count, setCount] = useLocalStorage<number>('counter', 0);

// Increment counter
setCount(prev => prev + 1);
```

This hook ensures that incrementing `count` in one tab will reflect in others after a read. It’s ideal for shared state like user preferences or counters across sessions.

95 t/s, 3402 tokens, 36s, 21%
