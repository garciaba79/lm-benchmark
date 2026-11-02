# Lfm2 24B A2B
Model: liquid/lfm2-24b-a2b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is a complete implementation of the `useLocalStorage` hook with detailed explanations.

### The Hook Implementation

```typescript
import { useState, useEffect, useCallback } from 'react';

/**
 * A custom React hook for managing state in localStorage with type safety.
 * 
 * @template T - The type of the value stored in localStorage.
 * @param {string} key - The key under which the value is stored.
 * @param {T} initialValue - The default value if no value exists in localStorage.
 * @returns {[T, (value: T) => void]} A tuple containing the current state and a setter function.
 */
export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  // State to hold the value
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      // Attempt to parse the value from localStorage
      const item = window.localStorage.getItem(key);
      if (item === null) {
        // If not found, return the initial value
        return initialValue;
      }
      // Parse and return the value
      return JSON.parse(item) as T;
    } catch (error) {
      // Handle parsing errors gracefully by falling back to initialValue
      console.warn(`Failed to parse localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Setter function that updates both state and localStorage
  const setValue = useCallback((value: T) => {
    try {
      // Convert value to JSON string and store it
      window.localStorage.setItem(key, JSON.stringify(value));
      // Update the state
      setStoredValue(value);
    } catch (error) {
      // Handle potential errors (e.g., quota exceeded)
      console.error(`Failed to save key "${key}":`, error);
      // Optionally: You could re-throw or handle differently here
    }
  }, [key]);

  // Effect to sync across tabs/windows when the value changes
  useEffect(() => {
    // Listen for storage events from other tabs/windows
    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === key && event.newValue !== null) {
        try {
          // Update state with the new value from localStorage
          setStoredValue(JSON.parse(event.newValue) as T);
        } catch (error) {
          console.error(`Error parsing storage event for key "${key}":`, error);
        }
      }
    };

    // Add event listener
    window.addEventListener('storage', handleStorageChange);

    // Cleanup: Remove the listener when the component unmounts or key changes
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key]);

  return [storedValue, setValue];
}
```

### Explanation of Key Features

1.  **Type Safety**: The generic type `T` ensures that the value stored in `localStorage` is always treated as that specific type. This prevents runtime errors when retrieving values.
2.  **Automatic JSON Handling**: The hook uses `JSON.stringify` and `JSON.parse` internally, abstracting this complexity from the component developer.
3.  **Error Handling**: Both reading (parsing) and writing operations are wrapped in `try/catch` blocks. If parsing fails (e.g., corrupted data), it falls back to the provided `initialValue`.
4.  **Cross-Tab Synchronization**: The `useEffect` hook listens for `storage` events. When another tab updates the value, the listener fires and updates the state in the current tab.
5.  **Cleanup**: The event listener is removed when the component unmounts or when the `key` changes, preventing memory leaks.
6.  **Initial Value Handling**: If no value exists for the key, it safely returns the `initialValue` provided to the hook.

### Benefits and Pros

*   **Reusability**: Eliminates repetitive boilerplate code for managing local storage across multiple components.
*   **Type Safety**: Reduces bugs by ensuring data is always handled as the correct type.
*   **Synchronization**: Provides a seamless experience where changes in one tab are instantly reflected in others, improving user experience.
*   **Encapsulation**: Hides the complexity of `localStorage` API (like error handling) behind a simple interface.

### Cons and Potential Issues

*   **Quota Limits**: Browsers impose limits on `localStorage` size (usually 5MB). If exceeded, writing will fail silently or throw an error.
*   **Synchronization Scope**: The `storage` event only fires for changes made in *other* tabs/windows. It does not trigger updates within the same tab if you manually change the value via the UI (it triggers on page load).
*   **Security**: `localStorage` is accessible via JavaScript, so sensitive data should never be stored here without encryption.
*   **Performance Overhead**: Parsing JSON on every read/write adds a slight overhead compared to direct access.

### Usage Example

```tsx
import { useLocalStorage } from './useLocalStorage';

function Counter() {
  const [count, setCount] = useLocalStorage<number>('counter', 0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

### Summary

The `useLocalStorage` hook provides a robust, type-safe way to manage persistent state in the browser. It abstracts away the complexities of the `localStorage` API while ensuring data integrity and synchronization across browser contexts. While it has minor limitations regarding quota and scope, its benefits for managing simple persistent data far outweigh these drawbacks in most use cases.

110 t/s, 1323 tokens, 13s, 9%
