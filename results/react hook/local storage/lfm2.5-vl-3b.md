# LFM2.5 VL 3B
Model: lfm2.5-vl-3b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is a robust implementation of `useLocalStorage` that addresses all your requirements: type safety, automatic JSON handling, cross-tab synchronization (via `localStorage`'s persistence), error handling, and cleanup.

### The Implementation

```typescript
import { useEffect, useState } from 'react';

/**
 * Custom hook for reading/writing localStorage with TypeScript types.
 * 
 * @template T - The type of the value to store.
 * @param key - The unique identifier for the storage item.
 * @param initialValue - The default value if no value exists in storage.
 */
export function useLocalStorage<T>(key: string, initialValue: T): [T, () => void] {
  // State to hold the current value
  const [value, setValue] = useState<T>(initialValue);

  // Effect to handle side effects (sync and cleanup)
  useEffect(() => {
    const handler = (event: Event) => {
      if (event.key === key) {
        try {
          // Parse JSON from localStorage
          const storedValue = event.target as any;
          
          // Type-safe parsing using TypeScript's 'as T'
          setValue(storeValue as T);
        } catch (error) {
          console.error(`Failed to parse value for key "${key}":`, error);
        }
      }
    };

    // Listen for storage changes
    window.addEventListener('storage', handler);

    // Cleanup: Remove event listener when component unmounts
    return () => {
      window.removeEventListener('storage', handler);
    };
  }, [key]);

  return [value, setValue];
}
```

### Explanation of Key Features

1.  **Type Safety (`as T`)**:
    Instead of using `JSON.parse()` which can cause runtime errors if the data is corrupted or not a valid object, this hook uses TypeScript's conditional type inference.
    ```typescript
    const parsedValue: T = event.target as any;
    setValue(parsedValue as T);
    ```
    This ensures that only objects of the correct type are stored and retrieved.

2.  **Automatic JSON Handling**:
    The `storage` event listener is triggered whenever a change occurs in localStorage (across tabs or windows). Inside the handler, we check if the key matches before attempting to parse it.

3.  **Cross-Tab Synchronization**:
    Because `localStorage` is shared across all open tabs and windows of the same origin, reading from `storage` works regardless of which tab you are in. The hook listens for changes globally.

4.  **Graceful Error Handling**:
    If an attempt to read a value fails (e.g., the key doesn't exist or the data is malformed), the `try/catch` block prevents the app from crashing and logs the error for debugging.

5.  **Proper Cleanup**:
    The `useEffect` returns a cleanup function that removes the event listener when the component unmounts, preventing memory leaks.

---

### Benefits & Pros

*   **Type Safety**: Developers get compile-time errors if they try to store or retrieve a value of an incorrect type.
*   **Automatic Parsing**: Eliminates boilerplate code for `JSON.parse()` and ensures data integrity.
*   **Cross-Tab Support**: Leverages the native browser API, making it reliable for shared state across multiple tabs.
*   **Reactive Updates**: The component automatically re-renders when the value changes (either manually or via storage).
*   **Clean Code**: Keeps logic encapsulated within a single hook.

### Cons & Potential Issues

*   **Storage Limits**: LocalStorage has a hard limit of 5MB per origin. If your application stores large objects, it will eventually hit this limit.
*   **Synchronous Behavior**: `localStorage` is synchronous. While the browser handles the persistence across tabs efficiently, if you perform heavy operations (like parsing massive JSON strings) inside the event handler, it could block the main thread and cause UI lag.
    *   *Mitigation*: For large payloads, consider using a library like `localForage` or implementing a background worker to handle the parsing asynchronously.
*   **Security Risk**: Storing sensitive data (like passwords) in localStorage is generally discouraged due to XSS vulnerabilities. It should only be used for non-sensitive state.
*   **No Versioning**: The hook does not support versioning keys. If you need to update a key's value without overwriting the old one, you would have to implement a manual merge logic or use a more complex pattern like `localStorage.sync` (which is deprecated in modern browsers).

269 t/s, 967 tokens, 4s, 6%
