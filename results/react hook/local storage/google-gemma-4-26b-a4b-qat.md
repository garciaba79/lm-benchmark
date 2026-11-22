# Gemma 4 26B A4B QAT
Model: google/gemma-4-26b-a4b-qat
Test: Hook Local Storage
Created: 11/22/2026, 03:08:58 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is a robust implementation of `useLocalStorage` using React 18 features, TypeScript, and the `storage` event for cross-tab synchronization.

### The Implementation

```typescript
import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * A custom hook to manage state in localStorage.
 * 
 * @param key - The key under which the value is stored in localStorage.
 * @param initialValue - The default value if no value is found in localStorage.
 */
export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((val: T) => T)) => void] {
  // 1. Get initial value from localStorage or use provided initialValue
  const readValue = useCallback((): T => {
    if (typeof window === 'undefined') return initialValue;

    try {
      const item = window.localStorage.getItem(key);
      // If item exists, parse it; otherwise use initialValue
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.warn(`Error reading localStorage key “${key}”:`, error);
      return initialValue;
    }
  }, [key, initialValue]);

  // Initialize state
  const [storedValue, setStoredValue] = useState<T>(readValue);

  // 2. The setter function
  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      // Allow value to be a function so we can do setVal(prev => !prev)
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      
      // Update state
      setStoredValue(valueToStore);

      // Save to localStorage
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
      }
    } catch (error) {
      console.error(`Error setting localStorage key “${key}”:`, error);
    }
  }, [key, storedValue]);

  // 3. Handle cross-tab synchronization
  useEffect(() => {
    const handleStorageChange = (event: StorageEvent) => {
      // Only update if the key matches the one we are watching
      if (event.key === key && event.newValue !== null) {
        try {
          setStoredValue(JSON.parse(event.newValue));
        } catch (error) {
          console.error(`Error parsing storage change for key “${key}”:`, error);
        }
      }
    };

    // Add event listener
    window.addEventListener('storage', handleStorageChange);

    // Cleanup: Remove listener on unmount
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [key]);

  return [storedValue, setValue];
}
```

### Usage Example

```tsx
const App = () => {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');

  return (
    <div style={{ background: theme === 'dark' ? '#333' : '#fff', color: theme === 'dark' ? '#fff' : '#333' }}>
      <p>Current Theme: {theme}</p>
      <button onClick={() => setTheme('light')}>Light Mode</button>
      <button onClick={() => setTheme('dark')}>Dark Mode</button>
      <button onClick={() => setTheme(prev => prev === 'light' ? 'dark' : 'light')}>Toggle</button>
    </div>
  );
};
```

---

### Explanation & Analysis

#### Benefits
1.  **Type Safety**: Using generics `<T>` ensures that the data retrieved is treated as the correct type, preventing runtime errors when accessing properties of objects.
2.  **Cross-Tab Syncing**: By listening to the `window` `storage` event, if a user changes the theme in Tab A, Tab B will immediately update its state without a refresh.
3.  **Functional Updates**: It supports functional updates (e.g., `setVal(prev => !prev)`), making it behave exactly like standard `useState`.
4.  **Error Resilience**: It uses `try/catch` blocks. If `localStorage` is disabled (e.g., Incognito mode in some browsers) or if the data is corrupted, the app falls back to `initialValue` instead of crashing.

#### Pros
*   **Zero Dependencies**: Keeps your bundle size minimal.
*   **Predictable**: Follows the standard React pattern for state management.
*   **Memory Efficient**: The event listener is properly cleaned up via the `useEffect` return function, preventing memory leaks.

#### Cons
*   **Serialization Overhead**: Every write involves `JSON.stringify` and every read involves `JSON.parse`. For massive objects or high-frequency updates (like tracking mouse position), this can cause UI lag.
*   **Storage Limits**: `localStorage` is limited (usually ~5MB). Attempting to store too much data will throw a `QuotaExceededError`.
*   **Synchronous Nature**: `localStorage` is a synchronous API. While it's fast, it blocks the main thread. For very large data chunks, `IndexedDB` is preferred.

#### Potential Issues & Edge Cases
1.  **SSR (Server Side Rendering)**: In frameworks like Next.js, `window` is not defined on the server. I have added `typeof window !== 'undefined'` checks to prevent "Window is not defined" errors.
2.  **Complexity of Data**: If you store complex objects like `Date` objects, `JSON.stringify` will turn them into strings. When you read them back, they will remain strings and won't be automatically converted back into `Date` objects.
3.  **Race Conditions**: In extremely high-speed environments where multiple components write to the same key simultaneously, there is a tiny window for race conditions, though the `storage` event largely mitigates this across tabs.

54 t/s, 1331 tokens, 25s, 9%
