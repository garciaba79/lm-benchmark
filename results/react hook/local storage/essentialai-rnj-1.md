# Rnj 1
Model: essentialai/rnj-1
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

It seems there is a misunderstanding in the problem statement since the requested hook `useLocalStorage<T>(key: string, initialValue: T)` should be written in TypeScript for a React application, not Python. I will provide you with the correct TypeScript implementation of the hook.

```typescript
import { useState, useEffect } from 'react';

function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  useEffect(() => {
    const handleStorageChange: EventListener = () => {
      try {
        const item = window.localStorage.getItem(key);
        setStoredValue(item ? JSON.parse(item) : initialValue);
      } catch (error) {
        console.error(error);
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => window.removeEventListener('storage', handleStorageChange);
  }, [key, initialValue]);

  const setValue = (value: T): void => {
    try {
      setStoredValue(value);
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}

export default useLocalStorage;
```

Benefits of this approach:
1. Type safety: TypeScript ensures that the data stored and retrieved from `localStorage` is of the correct type.
2. Automatic JSON parsing/stringifying: The hook handles the conversion between objects and strings automatically.
3. Sync across tabs/windows: Changes to the localStorage are reflected in all open tabs/windows using the `storage` event.
4. Error handling: Errors during storage operations are logged, ensuring that the application doesn't crash.

Pros:
- Clean and simple API for interacting with `localStorage`
- Automatic type safety
- Synchronization across multiple windows/tabs

Cons:
- Potential performance impact due to event listener on every window/tab change
- Possible race conditions in concurrent updates (though unlikely)
- Error handling might not be sufficient in production environments

Potential issues:
- The hook assumes that the initial value is a valid JSON object, which might not always be the case.
- It could be improved by providing an option to specify whether or not to sync across tabs/windows.

In conclusion, this `useLocalStorage` hook provides a robust and type-safe way to interact with `localStorage` in a React application.

119 t/s, 530 tokens, 5s, 4%
