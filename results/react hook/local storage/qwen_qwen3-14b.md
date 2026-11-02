# Qwen Qwen3 14B
Model: qwen_qwen3-14b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

### `useLocalStorage<T>` Hook Implementation

```tsx
import { useState, useEffect } from 'react';

/**
 * Custom React hook to manage localStorage with type safety and cross-tab syncing.
 * @param key - The key under which the value is stored in localStorage.
 * @param initialValue - The initial value to use if no value exists in localStorage.
 * @returns A tuple containing the current value and a function to update it.
 */
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((val: T) => T)) => void] {
  // Initialize state with value from localStorage or initial value
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      if (typeof window === 'undefined') return initialValue;
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error('Error reading from localStorage:', error);
      return initialValue;
    }
  });

  // Sync across tabs by listening to storage events
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === key) {
        try {
          const newValue = e.newValue ? JSON.parse(e.newValue) : null;
          setStoredValue(newValue as T);
        } catch (error) {
          console.error('Error parsing storage event value:', error);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key]);

  // Save to localStorage when storedValue changes
  useEffect(() => {
    try {
      if (typeof window === 'undefined') return;
      const valueToStore = JSON.stringify(storedValue);
      window.localStorage.setItem(key, valueToStore);
    } catch (error) {
      console.error('Error writing to localStorage:', error);
    }
  }, [key, storedValue]);

  return [storedValue, setStoredValue];
}

export default useLocalStorage;
```

---

### **Benefits**

1. **Type Safety with Generics**:
   - The hook uses TypeScript generics (`<T>`) to ensure type safety when reading from and writing to `localStorage`.

2. **Automatic JSON Parsing/Stringifying**:
   - Handles serialization/deserialization of values using `JSON.stringify` and `JSON.parse`, reducing boilerplate in components.

3. **Cross-Tab Synchronization**:
   - Listens for the `storage` event, ensuring changes made in one tab are reflected in others (within the same origin).

4. **Graceful Error Handling**:
   - Catches errors during parsing or writing operations and logs them without crashing the application.

5. **Proper Cleanup on Unmount**:
   - Removes the `storage` event listener when the component unmounts, preventing memory leaks.

6. **SSR Compatibility**:
   - Checks for the presence of `window` to avoid errors during server-side rendering (SSR).

---

### **Pros**

- **Centralized Logic**: Encapsulates localStorage logic in a single reusable hook.
- **Reduces Boilerplate**: Eliminates repetitive code for reading/writing to localStorage across components.
- **Consistent Data Handling**: Ensures consistent behavior between client and server (via SSR checks).
- **Type Safety**: Prevents runtime errors by enforcing type constraints with TypeScript.

---

### **Cons**

1. **Storage Size Limitations**:
   - `localStorage` has a size limit (~5MB per domain), which can be restrictive for large datasets.

2. **Performance Overhead**:
   - Frequent writes to `localStorage` may impact performance, especially in applications with high update frequency.

3. **Cross-Browser Compatibility**:
   - While widely supported, `localStorage` is not available in all environments (e.g., Safari Private Browsing mode).

4. **Type Mismatches**:
   - If the stored value does not match the expected type (`T`), TypeScript may cast it incorrectly, leading to runtime errors.

5. **SSR Limitations**:
   - Initial values used on the server do not reflect client-side `localStorage` data, which can cause discrepancies in SSR applications.

---

### **Potential Issues**

- **Circular References**: Attempting to store objects with circular references will throw an error during `JSON.stringify`. The hook catches this but does not prevent it.
  
- **Non-Serializable Values**: Functions or objects with non-serializable properties (e.g., `Date`, `RegExp`) may cause errors when parsed. Users must ensure values are serializable.

- **Same-Origin Policy**: Cross-origin tabs will not share `localStorage` data due to browser security policies.

---

### **Usage Example**

```tsx
import React from 'react';
import useLocalStorage from './useLocalStorage';

const App: React.FC = () => {
  const [theme, setTheme] = useLocalStorage('theme', 'dark');

  return (
    <div>
      <p>Current theme: {theme}</p>
      <button onClick={() => setTheme('light')}>Set Light</button>
      <button onClick={() => setTheme('dark')}>Set Dark</button>
    </div>
  );
};

export default App;
```

---

### **Conclusion**

The `useLocalStorage` hook provides a robust, type-safe solution for managing persistent data in React applications. It simplifies localStorage interactions while ensuring cross-tab synchronization and error resilience. However, developers should be mindful of its limitations (e.g., storage size, serialization constraints) when designing their applications.

10 t/s, 5759 tokens, 596s, 71%
