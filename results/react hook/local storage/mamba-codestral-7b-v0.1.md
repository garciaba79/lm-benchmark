# Mamba Codestral 7B v0.1
Model: mamba-codestral-7b-v0.1
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 32K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

```typescript
import { useState, useEffect } from 'react';

function useLocalStorage<T>(key: string, initialValue: T) {
    // State to store our value
    const [storedValue, setStoredValue] = useState(() => {
        try {
            // Get from local storage by key
            const item = window.localStorage.getItem(key);
            // Parse stored json or if none return initialValue
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.log(error);
            return initialValue;
        }
    });

    useEffect(() => {
        try {
            // Allow value to be a function so we have same API as useState
            const valueToStore = typeof storedValue === 'function' ? storedValue() : storedValue;
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.log(error);
        }
    }, [storedValue]);

    useEffect(() => {
      const handleStorageChange = (e: StorageEvent) => {
        if (e.key === key && e.newValue !== null) {
          setStoredValue(JSON.parse(e.newValue));
        }
      };

      window.addEventListener('storage', handleStorageChange);

      return () => {
        window.removeEventListener('storage', handleStorageChange);
      };
    }, [key]);

    const setValue = (value: T | ((val: T) => T)) => {
        try {
            // Allow value to be a function so we have same API as useState
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
            setStoredValue(value);
        } catch (error) {
            console.log(error);
        }
    };

    return [storedValue, setValue];
}
```
Benefits:
1. Type safety - We use generics to ensure that the initial value and stored value are of the same type. This helps in catching errors at compile time rather than runtime.
2. Automatic JSON parsing/stringifying - The hook automatically handles serialization and deserialization, allowing us to store complex objects in local storage without having to manually parse or stringify them.
3. Sync across tabs/windows - By listening for the 'storage' event on window, we can ensure that changes made by other tabs/windows are reflected in our state. This is useful when multiple tabs of a web app need to share data stored in local storage.
4. Error handling - The hook includes error handling both while reading from and writing to local storage. If an error occurs during these operations, it will be caught and logged to the console, preventing the application from crashing due to unhandled exceptions.

Pros:
1. Easy to use - The hook provides a simple API for getting and setting values in local storage, with automatic JSON parsing/stringifying and type safety.
2. Sync across tabs/windows - By listening for the 'storage' event on window, we can ensure that changes made by other tabs/windows are reflected in our state. This is useful when multiple tabs of a web app need to share data stored in local storage.
3. Error handling - The hook includes error handling both while reading from and writing to local storage. If an error occurs during these operations, it will be caught and logged to the console, preventing the application from crashing due to unhandled exceptions.

Cons:
1. Limited browser support - The 'storage' event is not supported in Internet Explorer or Safari. This means that changes made by other tabs/windows may not be reflected in our state on these browsers.
2. Storage limits - Local storage has a limit of 5MB per domain, which can be reached quickly if the data stored in it is large. If this limit is exceeded, storing more data will result in loss of older data.
3. Security concerns - Storing sensitive information in local storage can pose security risks as it's easily accessible to attackers. It should not be used for storing passwords or other confidential data.

Potential issues:
1. Browser support - As mentioned earlier, the 'storage' event is not supported in Internet Explorer or Safari. This means that changes made by other tabs/windows may not be reflected in our state on these browsers.
2. Storage limits - Local storage has a limit of 5MB per domain, which can be reached quickly if the data stored in it is large. If this limit is exceeded, storing more data will result in loss of older data.
3. Security concerns - Storing sensitive information in local storage can pose security risks as it's easily accessible to attackers. It should not be used for storing passwords or other confidential data.

139 t/s, 1116 tokens, 8s, 4%
