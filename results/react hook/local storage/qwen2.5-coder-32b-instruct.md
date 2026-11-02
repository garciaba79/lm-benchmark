# Qwen2.5 Coder 32B Instruct
Model: qwen2.5-coder-32b-instruct
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Sure! Below is a TypeScript implementation of the `useLocalStorage` hook for React 18+:

```typescript
import { useState, useEffect, useCallback } from 'react';

function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((prevValue: T) => T)) => void] {
    const readValue = useCallback((): T => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.warn(`Error reading localStorage key "${key}":`, error);
            return initialValue;
        }
    }, [initialValue, key]);

    const [storedValue, setStoredValue] = useState<T>(readValue);

    useEffect(() => {
        try {
            const handleStorageChange = (event: StorageEvent) => {
                if (event.key && event.key !== key) {
                    return;
                }
                setStoredValue(readValue());
            };

            window.addEventListener('storage', handleStorageChange);
            return () => window.removeEventListener('storage', handleStorageChange);
        } catch (error) {
            console.warn(`Error setting up storage listener for key "${key}":`, error);
        }
    }, [key, readValue]);

    const setValue = useCallback((value: T | ((prevValue: T) => T)) => {
        try {
            // Allow value to be a function so we have the same API as useState
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.warn(`Error setting localStorage key "${key}":`, error);
        }
    }, [key, storedValue]);

    return [storedValue, setValue];
}

export default useLocalStorage;
```

### Explanation:

1. **`readValue` Function:**
   - This function reads the value from `localStorage`. If it exists, it parses it as JSON; otherwise, it returns the initial value.
   - It's wrapped in a `useCallback` to prevent re-creating the function on every render.

2. **State Initialization:**
   - The state is initialized with the value read from `localStorage`.

3. **Storage Event Listener:**
   - An event listener is added to listen for changes across different tabs/windows.
   - If the key matches, it updates the local state with the new value.
   - Cleanup function removes the event listener when the component unmounts.

4. **`setValue` Function:**
   - This function updates the state and sets the new value in `localStorage`.
   - It can take a function as an argument, just like `useState`.

### Benefits:
- **Automatic JSON Parsing/Stringifying:** Simplifies storing and retrieving complex data structures.
- **Type Safety:** Ensures that the data type is consistent with the generic type `T`.
- **Sync Across Tabs/Windows:** Automatically updates state when changes are made in other tabs or windows.
- **Error Handling:** Gracefully handles errors during read/write operations, preventing app crashes.

### Pros:
- **Simplifies Local Storage Management:** Reduces boilerplate code for reading and writing to local storage.
- **Cross-tab Synchronization:** Ensures data consistency across different browser tabs/windows.
- **Type-safe:** Leverages TypeScript's type system for better safety and developer experience.

### Cons:
- **Performance Overhead:** Parsing and stringifying JSON can be computationally expensive, especially with large objects.
- **Limited Storage Size:** Local storage has a size limit (typically 5-10 MB), so it may not be suitable for large datasets.
- **Data Inconsistency:** If the data structure changes over time, it might lead to inconsistencies or errors during parsing.

### Potential Issues:
- **Security Risks:** Storing sensitive information in local storage can pose security risks. Ensure proper validation and sanitization.
- **Concurrency Issues:** Multiple writes within a short period may cause race conditions. Consider using transactional patterns if necessary.
- **Browser Compatibility:** Although `localStorage` is widely supported, ensure compatibility with older browsers if needed.

This hook provides a robust solution for managing local storage in React applications while maintaining type safety and handling common edge cases.

6 t/s, 891 tokens, 160s, 6%
