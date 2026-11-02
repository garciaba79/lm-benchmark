# Qwen3.5 4B
Model: qwen3.5-4b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

```tsx
import { useState, useEffect } from 'react';

/**
 * useLocalStorage Hook
 * 
 * Provides a type-safe way to persist state to localStorage with automatic JSON handling.
 * It includes cross-tab synchronization via the StorageEvent API and handles errors gracefully.
 */
export function useLocalStorage<T>(key: string, initialValue: T) {
  // Initialize state from localStorage on mount
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      if (typeof window !== 'undefined') {
        const item = window.localStorage.getItem(key);
        return item ? JSON.parse(item) : initialValue;
      }
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Effect to write value back to localStorage whenever it changes
  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.warn(`Error writing to localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);

  // Effect to listen for changes made by other tabs/windows
  useEffect(() => {
    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === key && event.newValue !== null) {
        try {
          const parsedValue = JSON.parse(event.newValue);
          setStoredValue(parsedValue);
        } catch (error) {
          console.warn(`Error parsing storage value for key "${key}":`, error);
        }
      }
    };

    // Add listener on mount
    window.addEventListener('storage', handleStorageChange);

    // Cleanup function to remove listener on unmount or key change
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key]);

  const setValue = (value: T) => {
    setStoredValue(value);
  };

  return [storedValue, setValue] as const;
}
```

### Explanation & Analysis

#### Benefits
1.  **Type Safety:** By using the generic `<T>`, TypeScript ensures that the value stored matches the expected type. If you try to store a string where an object is expected, it will throw a compile-time error.
2.  **Cross-Tab Sync:** Unlike simple state hooks, this hook listens for `StorageEvent`. This means if Tab A updates the data, Tab B (and other windows) automatically detects and syncs without manual polling or complex event listeners.
3.  **Error Resilience:** It wraps all storage operations in try/catch blocks to prevent React from crashing due to quota exceeded errors, CORS issues, or invalid JSON parsing.
4.  **No Dependencies:** Pure React implementation using only `useState` and `useEffect`.

#### Pros
*   **Simplicity:** Usage is as simple as `<MyComponent useLocalStorage="user-preferences" />`.
*   **Performance:** Minimal overhead; no heavy polling logic, just direct storage access.
*   **Type Safety:** Prevents runtime type mismatches (e.g., storing a number when an object was expected).

#### Cons & Potential Issues
1.  **Browser Quota Limits:** `localStorage` has a hard limit (typically 5MB per domain). Storing large arrays or objects will eventually fail, potentially causing the app to crash if not handled gracefully.
2.  **Security Risks (XSS):** If you store sensitive data in localStorage and render it directly on the client side without sanitization, it could be vulnerable to Cross-Site Scripting attacks.
3.  **No Server Sync:** This is purely client-side. It does not sync with a backend database. If the user clears their cache or uses incognito mode, data is lost.
4.  **`storage` Event Limitations:** The `StorageEvent` only fires in the browser tab that *initiated* the write (the one writing to storage). However, because we are listening for changes made by other tabs, it works correctly for cross-tab sync. Note: Some older browsers or specific configurations might not support this event reliably.
5.  **Race Conditions:** If multiple tabs update simultaneously, there is a slight race condition where the last write wins (standard localStorage behavior).

#### Usage Example
```tsx
import { useLocalStorage } from './useLocalStorage';

function UserProfile() {
  const [user, setUser] = useLocalStorage<User>('user-profile', { name: 'Guest' });

  return (
    <div>
      <h1>Hello, {user.name}</h1>
      <button onClick={() => setUser({ ...user, name: 'John Doe' })}>Update Name</button>
    </div>
  );
}
```

161 t/s, 3160 tokens, 20s, 20%
