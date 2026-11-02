# Phi 4
Model: microsoft/phi-4
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Creating a custom hook like `useLocalStorage<T>` in TypeScript for managing local storage with automatic JSON parsing/stringifying can be quite useful. Below is an implementation of this hook along with an explanation of its benefits, advantages, disadvantages, and potential issues.

### Implementation

```tsx
import { useState, useEffect } from 'react';

function useLocalStorage<T>(key: string, initialValue: T): [T | null, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T | null>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error parsing localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  useEffect(() => {
    function handleStorageChange(event: StorageEvent) {
      if (event.key === key) {
        try {
          const newValue = event.newValue ? JSON.parse(event.newValue) : null;
          setStoredValue(newValue);
        } catch (error) {
          console.error(`Error parsing updated localStorage value for key "${key}":`, error);
        }
      }
    }

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key]);

  const setValue = (value: T) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  };

  return [storedValue, setValue];
}

export default useLocalStorage;
```

### Explanation

1. **Type Safety**: The hook is generic with `T` allowing type-safe operations on the stored data.

2. **Automatic JSON Parsing/Stringifying**: 
   - On initial load and whenever setting a value, JSON parsing/stringifying is handled automatically.
   - This reduces boilerplate code and potential human errors during manual conversions.

3. **Sync Across Tabs/Windows**:
   - Uses the `StorageEvent` to listen for changes in local storage from other tabs/windows.
   - Automatically updates the state when another tab/window modifies the same key.

4. **Error Handling**:
   - Catches and logs any JSON parsing errors during initial load or upon receiving a storage event.
   - Handles exceptions when setting an item in localStorage, ensuring application stability.

5. **Cleanup on Unmount**:
   - Removes the `storage` event listener when the component unmounts to prevent memory leaks or unwanted behavior.

### Benefits

- **Type Safety**: Ensures that you work with the correct types throughout your code.
- **Ease of Use**: Abstracts away repetitive JSON operations and synchronizes state across tabs/windows automatically.
- **Error Handling**: Gracefully handles errors without crashing the application, improving robustness.
- **Reusability**: Can be easily reused across different components within an application.

### Pros

- Reduces boilerplate code for managing local storage.
- Keeps UI in sync with changes made from other tabs or windows.
- Provides type safety and error handling out of the box.

### Cons

- **Performance**: Listening to `storage` events can lead to performance overhead if there are frequent updates, although this is generally negligible for most use cases.
- **Limited Scope**: Works only within the same origin due to browser security restrictions on localStorage.
- **Storage Limitations**: Local storage has a size limit (usually around 5MB per domain), which might not be suitable for storing large datasets.

### Potential Issues

- **Cross-Domain Usage**: This hook will not work across different domains, as `localStorage` is scoped per origin.
- **Sensitive Data**: Storing sensitive information in localStorage can be risky since it's accessible by any script running on the page. It should be used carefully for non-sensitive data.
- **Browser Compatibility**: While most modern browsers support localStorage, some older or less common browsers might not.

This hook provides a robust and type-safe way to manage local storage within React applications using functional components.

75 t/s, 847 tokens, 11s, 6%
