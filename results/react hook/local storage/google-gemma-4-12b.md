# Gemma 4 12B
Model: google/gemma-4-12b
Test: Hook Local Storage
Created: 11/03/2026, 01:01:47 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is a production-ready implementation of a `useLocalStorage` hook.

### The Implementation

```typescript
import { useState, useEffect, useCallback } from 'react';

/**
 * A custom hook to manage state synced with localStorage.
 * @param key - The key under which the value is stored in localStorage.
 * @param initialValue - The default value if the key does not exist in storage.
 * @returns The current value and a setter function.
 */
export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((prev: T) => T)) => void] {
  // Initialize state from localStorage or use the provided default
  const [storedValue, set_state] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      // If the item exists and is not null/empty, parse it; otherwise return initialValue
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Update the value in localStorage and local state
  const setValue = useCallback((value: T | ((prev: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      
      // Sync with LocalStorage
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
      
      // Update local state to trigger re-render
      set_state(valueToStore);
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key]);

  // Effect to handle cross-tab synchronization
  useEffect(() => {
    const handleStorageChange = (event: StorageEvent) => {
      // Only update if the changed key matches our key and the value is different
      if (event.key === key && event.newValue !== null) {
        try {
          set_state(JSON.parse(event.newValue) as T);
        } catch (e) {
          console.error(`Error parsing storage change for "${key}":`, e);
        }
      }
    };

    // Add event listener for changes in other tabs/windows
    window.addEventListener('storage', handleStorageChange);
    
    // Cleanup listener on unmount
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [key]);

  return [storedValue, setValue] as [T, (value: T | ((prev: T) => T)) => void];
}
```

---

### Explanation & Analysis

#### Key Features Included:
1.  **Type Safety:** Uses TypeScript Generics `<T>` to ensure the value returned by the hook matches your expected type (e.g., an object, array, or primitive).
2.  **Lazy Initialization:** The `useState` initializer is only executed on the first render, preventing expensive JSON parsing logic from running every time the component re-renders.
3.  **Cross-Tab Sync:** It listens to the window `storage` event. When a user changes a value in Tab A, your app in Tab B will automatically update its state.
4.  **Robust Error Handling:** Wrapped in `try/catch` blocks to handle cases where `localStorage` is full (QuotaExceededError) or if the data stored is corrupted/not valid JSON.
5.  **Functional Updates:** The setter supports functional updates (e.g., `setValue(prev => [...prev, newItem])`), which is standard for React's `useState`.

#### Pros:
*   **Persistence:** State survives page refreshes.
*   **Syncing:** Real-time synchronization across browser tabs makes it great for settings (like "Dark Mode" or "Auth Tokens").
*   **Zero Dependencies:** No extra bundle size from external libraries.
*   **Type Safety:** Ensures that if you tell the hook the value is a `User` object, TypeScript will enforce that type throughout your component.

#### Cons:
*   **Blocking Execution:** LocalStorage is synchronous. While rarely an issue for small strings, very large amounts of data can theoretically block the main thread during read/write operations.
*   **String-Only Storage:** Since it uses `JSON.stringify`, complex types like `Map`, `Set`, or functions cannot be stored directly (they will turn into empty objects `{}`).

#### Potential Issues & Considerations:
1.  **SSR (Server Side Rendering):** If using Next.js or any SSR framework, this hook will crash on the server because `window` is not defined. 
    *   *Fix:* Wrap the initial state logic in a check for `typeof window !== 'undefined'`.
2.  **Storage Limits:** Browsers typically limit LocalStorage to ~5MB. If you exceed this, `setItem` will throw an error (handled by our `try/catch`, but the data won't save).
3.  **Security:** Never store sensitive information like plain-text passwords or PII (Personally Identifiable Information) in `localStorage`. It is accessible by any script running on your page (XSS risk).
4.  **JSON limitations:** If you store a Date object, it will be returned as a String after being parsed from JSON unless you manually handle the conversion back to a Date object.

81 t/s, 1200 tokens, 15s
