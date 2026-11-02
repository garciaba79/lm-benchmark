# Qwen2.5 Coder 14B
Model: qwen/qwen2.5-coder-14b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here's a TypeScript implementation of the `useLocalStorage` hook in React:

```typescript
import { useState, useEffect } from 'react';

function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  const readValue = () => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.warn(`Error reading localStorage key “${key}”:`, error);
      return initialValue;
    }
  };

  const [storedValue, setStoredValue] = useState<T>(readValue);

  useEffect(() => {
    setStoredValue(readValue());
  }, [key]);

  const setValue = (value: T | ((prevState: T) => T)) => {
    try {
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
      setStoredValue(valueToStore);
      window.dispatchEvent(new StorageEvent('storage', { key }));
    } catch (error) {
      console.warn(`Error setting localStorage key “${key}”:`, error);
    }
  };

  useEffect(() => {
    const handleStorageChange = () => {
      if (window.event.key === key) {
        setStoredValue(readValue());
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key]);

  return [storedValue, setValue];
}

export default useLocalStorage;
```

### Explanation:

1. **Initialization**:
   - `readValue` function reads the value from localStorage, parses it (if exists), or returns the initial value if an error occurs.
   - The `useState` hook is used to store the current value in component state.

2. **Effect for Initial Value**:
   - An effect runs once on mount to set the initial state using `readValue`.

3. **State Update Function (`setValue`)**:
   - Handles both direct and functional updates.
   - Strings the new value to localStorage.
   - Updates the local state.
   - Dispatches a custom storage event to notify other tabs/windows of the change.

4. **Effect for Cross-Tab Syncing**:
   - Adds a `storage` event listener that updates the component's state when another tab/window writes to the same key.
   - Cleans up the event listener on unmount.

### Benefits:

1. **Type Safety**: TypeScript generics ensure that the value returned and updated is of the expected type.
2. **Automatic JSON Handling**: Automatically parses strings from localStorage and serializes objects before writing.
3. **Cross-Tab Syncing**: Keeps values in sync across different tabs or windows by listening to `storage` events.

### Pros:

1. **Reusability**: Can be used across multiple components for any type of data (strings, numbers, objects).
2. **Simplicity**: No external libraries required, leveraging built-in browser features.
3. **Error Handling**: Gracefully handles errors during read/write operations without breaking the application.

### Cons:

1. **Performance**: Writing to localStorage can be slow, especially for large datasets. For high-performance applications, consider using IndexedDB instead.
2. **Limitations on Storage Size**: Each origin is limited to 5-10MB of storage. For large datasets, use Web APIs like IndexedDB.

### Potential Issues:

1. **Cross-Origin Limitations**: The `storage` event only triggers for the same origin. Different subdomains or protocols won't receive events.
2. **Security Concerns**: Avoid storing sensitive information in localStorage due to potential exposure through client-side code.
3. **Race Conditions**: In multi-threaded environments, concurrent writes might lead to race conditions. Implementing a more sophisticated conflict resolution strategy may be necessary.

This hook provides a robust and flexible solution for managing state with localStorage in React applications while ensuring type safety and cross-tab synchronization.

72 t/s, 829 tokens, 12s, 6%
