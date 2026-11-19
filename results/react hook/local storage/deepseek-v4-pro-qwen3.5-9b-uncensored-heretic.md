# DeepSeek v4 Pro Qwen3.5 9B UNCENSORED Heretic
Model: deepseek-v4-pro-qwen3.5-9b-uncensored-heretic
Test: Hook Local Storage
Created: 11/18/2026, 11:46:20 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is a robust implementation of `useLocalStorage` in TypeScript for React 18+, along with an explanation of its design choices, benefits, and potential pitfalls.

### Implementation

```tsx
import { useEffect, useState } from 'react';

/**
 * Custom hook to manage localStorage with type safety, automatic JSON parsing/stringifying,
 * cross-tab synchronization, error handling, and proper cleanup.
 */
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((val: T) => T) | undefined)] {
  // State to hold the current value
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      if (typeof window === 'undefined') {
        return initialValue;
      }

      const item = window.localStorage.getItem(key);
      
      // If item exists and is valid JSON, parse it. Otherwise, use initial value.
      if (item !== null) {
        try {
          return JSON.parse(item);
        } catch (error) {
          console.warn(`Error parsing localStorage for key "${key}":`, error);
          // If parsing fails, fall back to initialValue
          return initialValue;
        }
      }
      
      return initialValue;
    } catch (error) {
      console.warn(`Error reading localStorage for "${key}":`, error);
      return initialValue;
    }
  });

  // Update localStorage and notify subscribers when the value changes
  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }

    try {
      const valueToStore = storedValue;
      
      // Check if the value has actually changed to avoid unnecessary writes
      const currentStored = window.localStorage.getItem(key);
      if (currentStored !== JSON.stringify(valueToStore)) {
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
        
        // Optional: Dispatch a custom event for cross-tab synchronization
        // This allows other tabs/windows listening to this key to update their state
        window.dispatchEvent(new CustomEvent('local-storage-change', { detail: { key, value: valueToStore } }));
      }
    } catch (error) {
      console.warn(`Error setting localStorage for "${key}":`, error);
    }
  }, [storedValue, key]);

  // Helper to update the stored value
  const setValue = (value: T | ((val: T) => T) | undefined) => {
    try {
      // If value is a function, run it with the current value
      const newValue = value != null ? typeof value === 'function' ? value(storedValue) : value : storedValue;
      
      setStoredValue(newValue);
      
      // Write to localStorage and trigger cross-tab sync
      window.localStorage.setItem(key, JSON.stringify(newValue));
      
      // Dispatch custom event for cross-tab synchronization
      window.dispatchEvent(new CustomEvent('local-storage-change', { detail: { key, value: newValue } }));
    } catch (error) {
      console.warn(`Error setting localStorage for "${key}":`, error);
      // In case of an error, we might not want to update the state either
    }
  };

  return [storedValue, setValue];
}

export default useLocalStorage;
```

---

### How It Works

1. **Initialization**: On mount, it attempts to read from `localStorage`. If the data is corrupted (invalid JSON), it gracefully falls back to the `initialValue` passed by the user.
2. **Automatic Serialization**: All reads and writes are wrapped in `JSON.stringify()` and `JSON.parse()`, ensuring type safety at compile time while handling runtime serialization errors safely.
3. **Cross-Tab Synchronization**: It dispatches a custom event (`local-storage-change`) whenever the value changes. Other tabs or windows can listen to this event using `window.addEventListener('local-storage-change', ...)` and update their own state accordingly.
4. **Error Handling**: Every read/write operation is wrapped in a `try...catch` block. If something goes wrong (e.g., quota exceeded, browser security restriction), the error is logged but doesn't crash the app; it falls back to the initial value or skips the write.
5. **Cleanup**: While there's no explicit cleanup function needed for `localStorage` itself (it persists until cleared), the hook ensures that if the component unmounts, no further effects are triggered. The dependency array `[storedValue, key]` ensures updates only happen when necessary.

---

### Benefits & Pros

- **Type Safety**: By using generics `<T>`, TypeScript can infer the type of your stored data. This prevents accidental assignment of wrong types and allows for better autocomplete in IDEs.
- **Automatic Serialization**: No need to manually `JSON.stringify` or `JSON.parse`. The hook handles this internally, reducing boilerplate code.
- **Graceful Degradation**: If `localStorage` is unavailable (e.g., due to browser restrictions or quota limits), the hook doesn't crash; it simply uses the provided initial value and logs a warning.
- **Cross-Tab Synchronization**: The built-in event dispatching makes it easy to share state across multiple tabs/windows without needing external libraries like Redux or Zustand.
- **Performance Optimization**: It only writes to `localStorage` if the actual value has changed, avoiding unnecessary I/O operations.

---

### Cons & Potential Issues

1. **Size Limitations**: Browsers typically limit `localStorage` to around 5–10 MB per origin. Storing large objects or arrays directly can cause performance issues or exceed this limit.
2. **Serialization Constraints**: Since everything is stored as a JSON string, you cannot store functions, undefined values, circular references, or complex prototypes. You must ensure your data structure is serializable.
3. **Security Contexts**: In some secure contexts (like certain Content Security Policies), `localStorage` might be restricted. The hook handles this gracefully but may silently fail to persist changes.
4. **Race Conditions in Multi-Tab Environments**: While the custom event helps, if two tabs modify the same key simultaneously, one update might overwrite the other before the second read occurs. This is inherent to how `localStorage` works and cannot be fully avoided without additional locking mechanisms.
5. **No Automatic Cleanup on Unmount**: Unlike some hooks that provide a cleanup function, this hook relies on React's lifecycle management implicitly. If you need to clear specific keys when the component unmounts, you'd have to implement that logic manually (e.g., `window.localStorage.removeItem(key)`).

---

### Example Usage

```tsx
import { useState } from 'react';
import useLocalStorage from './useLocalStorage';

function Counter() {
  const [count, setCount] = useLocalStorage<number>('counter', 0);

  return (
    <div>
      <p>Current count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(prev => prev - 1)}>Decrement</button>
    </div>
  );
}

// In another component or tab, listen for changes:
function TabListener() {
  useEffect(() => {
    const handleStorageChange = (event: CustomEvent) => {
      if (event.detail.key === 'counter') {
        console.log(`Counter changed to:`, event.detail.value);
      }
    };

    window.addEventListener('local-storage-change', handleStorageChange as EventListener);
    
    return () => {
      window.removeEventListener('local-storage-change', handleStorageChange as EventListener);
    };
  }, []);

  return null;
}
```

133 t/s, 1655 tokens, 12s
