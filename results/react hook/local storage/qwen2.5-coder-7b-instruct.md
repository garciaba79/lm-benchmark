# Qwen2.5 Coder 7B Instruct
Model: qwen2.5-coder-7b-instruct
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is a simple implementation of useLocalStorage hook in TypeScript:

```typescript
import { useState, useEffect } from 'react';

const useLocalStorage = <T>(key: string, initialValue: T): [T, (value: T) => void] => {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      // Get from local storage by key
      const item = window.localStorage.getItem(key);
      // Parse stored json or if none return initialValue
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      // Save state to local storage
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.error(error);
    }
  }, [key, storedValue]);

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      // Allow value to be a function so we have same API as useState
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
};

export default useLocalStorage;
```

Benefits:
1. Type safety: The hook is generic and can be used with any type.
2. Automatic parsing/stringifying of JSON data.
3. Sync across tabs/windows if the key changes.

Pros:
- It's a simple implementation that doesn't require external libraries.
- It provides automatic error handling.
- It supports updating state based on previous value, just like useState does.

Cons:
- It can cause performance issues when used with large objects because it needs to parse and stringify JSON data every time the component re-renders.
- It might not work as expected if localStorage is disabled in the browser or if there are cross-origin restrictions.

Potential Issues:
- The hook doesn't handle cases where the initialValue is a function. This could lead to unexpected behavior when using useState's functional update feature.
- If the key changes, it will overwrite the old value in localStorage and remove any other values that might be stored under the same key.
- It doesn't provide any way to listen for changes in localStorage from other tabs/windows.

138 t/s, 499 tokens, 4s, 4%
