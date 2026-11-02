# Ministral 3 3B Reasoning 2512
Model: ministral-3-3b-reasoning-2512
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 32K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is the `useLocalStorage` hook in TypeScript for React 18+:

```typescript
import { useState, useEffect } from 'react';

function useLocalStorage<T>(key: string, initialValue: T) {
    // Check if localStorage is available in the current environment
    const isLocalStorageAvailable = typeof window !== 'undefined' && window.localStorage;

    // Initialize state with the value from localStorage or the initialValue
    const [storedValue, setStoredValue] = useState<T>(() => {
        if (!isLocalStorageAvailable) {
            return initialValue;
        }
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error('Error reading from localStorage:', error);
            return initialValue;
        }
    });

    // Function to set the value in localStorage and update state
    const setValue = (value: T) => {
        if (!isLocalStorageAvailable) {
            console.warn('localStorage is not available');
            return;
        }
        try {
            window.localStorage.setItem(key, JSON.stringify(value));
            setStoredValue(value);
        } catch (error) {
            console.error('Error writing to localStorage:', error);
        }
    };

    // Listen for storage events to sync when the key changes in other tabs
    useEffect(() => {
        const handleStorage = () => {
            if (!isLocalStorageAvailable) return;
            try {
                const item = window.localStorage.getItem(key);
                setStoredValue(item ? JSON.parse(item) : initialValue);
            } catch (error) {
                console.error('Error reading from localStorage on storage event:', error);
            }
        };

        if (isLocalStorageAvailable) {
            window.addEventListener('storage', handleStorage);

            return () => {
                // Cleanup: remove the event listener when component unmounts
                window.removeEventListener('storage', handleStorage);
            };
        }

    }, [key, initialValue]);

    return [storedValue, setValue];
}
```

### Explanation and Considerations

**Benefits:**
- **Type Safety**: The generic type `T` ensures that the stored value is of the correct type, preventing type mismatches.
- **Automatic JSON Handling**: The hook automatically parses and stringifies values to/from localStorage, simplifying usage for common types (strings, numbers, objects, arrays).
- **Error Handling**: Errors during reading or writing are caught and logged, ensuring the component remains stable even if localStorage is unavailable or if JSON parsing fails.
- **Cleanup on Unmount**: The event listener is removed when the component unmounts to prevent memory leaks.

**Pros:**
- Simple API for common use cases (e.g., storing and retrieving values).
- Works with any type that can be serialized to JSON, such as strings, numbers, objects, and arrays.
- Gracefully handles cases where localStorage is not available in the current environment (like private browsers).

**Cons:**
- **Limited by localStorage**: LocalStorage has a size limit (typically 5MB per domain) and is not available in all environments (e.g., private browsers). It is also not synced across different domains or tabs/windows unless they are in the same domain.
- **Event Listener Overhead**: Listening to 'storage' events for all keys can be inefficient if there are many keys being frequently updated. However, this is unavoidable since localStorage does not provide a way to listen for changes to a specific key.
- **JSON Serialization Constraints**: The hook assumes that the initial value and any set values are JSON-serializable. If they are not (e.g., functions or custom objects without proper serialization), it will throw an error.

**Potential Issues:**
1. **JSON Parsing Errors**: If the stored value is not valid JSON, parsing will fail. This can happen if the initial value or any set value is not serializable.
2. **localStorage Unavailable**: In some environments (like private browsers), localStorage might be disabled. The hook handles this by returning the initial value and warning when setting values.
3. **Event Listener Leak**: If the component unmounts without cleaning up, the event listener might remain. However, our useEffect has a cleanup function to remove it, so this should not happen in normal usage.
4. **Performance**: Listening to all storage events can be heavy if there are many keys being changed frequently. In such cases, it might be better to only listen for changes to the specific key (though localStorage does not provide an event for a single key; you must listen for all storage events and check which key was changed).

### Example Usage

```typescript
function Counter() {
    const [count, setCount] = useLocalStorage<number>('count', 0);

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>Increment</button>
        </div>
    );
}
```

This hook is useful for managing state that should persist across component unmounts and remounts, as well as when the same key is used in different tabs of the same domain. However, it is not a substitute for server-side state management or for more complex state needs.

193 t/s, 4976 tokens, 26s, 16%
