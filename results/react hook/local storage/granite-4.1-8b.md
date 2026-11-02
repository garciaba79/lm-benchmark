# Granite 4.1 8B
Model: granite-4.1-8b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

### `useLocalStorage<T>(key: string, initialValue: T)` Hook Implementation

```typescript
import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook to interact with localStorage in a type-safe manner.
 *
 * @param key The storage key to use in localStorage.
 * @param initialValue The initial value for the state when no stored value is found.
 * @returns A tuple containing the current value and a setter function.
 */
export const useLocalStorage = <T>(key: string, initialValue: T): [T, (value: T | ((val: T) => T)) => void] => {
  // State to hold the current value
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      // Attempt to parse and retrieve the stored JSON value
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      // If parsing fails, fallback to the initial value and log an error
      console.error('Error parsing localStorage:', error);
      return initialValue;
    }
  });

  // Function to update storedValue and localStorage
  const setValue = useCallback(
    (value: T | ((val: T) => T)) => {
      try {
        const valueToStore =
          typeof value === 'function' ? value(storedValue) : value;

        // Stringify the value before storing it in localStorage
        window.localStorage.setItem(key, JSON.stringify(valueToStore));

        // Update state with the new value
        setStoredValue(valueToStore);
      } catch (error) {
        // Log any errors that occur during storage or stringification
        console.error('Error setting localStorage:', error);
      }
    },
    [key, storedValue]
  );

  // Cleanup effect to remove event listeners if necessary
  useEffect(() => {
    const handler = ({ newValue }: { newValue: boolean }) => {
      // Sync value across tabs/windows when the key changes
      setValue(storedValue);
    };

    window.addEventListener('storage', handler);

    // Return a cleanup function to remove the event listener on unmount
    return () => {
      window.removeEventListener('storage', handler);
    };
  }, [key, storedValue, setValue]);

  return [storedValue, setValue];
};
```

### Explanation

- **Type Safety**: The generic type `<T>` ensures that the value stored and retrieved from localStorage matches the specified type at compile time.
- **Initial Value Handling**: If the key does not exist in localStorage or parsing fails (e.g., due to invalid JSON), `initialValue` is used, ensuring a graceful fallback.
- **Sync Across Tabs/Windows**: By listening for the `storage` event on `window`, changes made by other tabs/windows that affect the same key trigger an update of the stored value in this component.
- **Error Handling**: Both parsing from localStorage and stringifying before storage are wrapped in try-catch blocks to prevent runtime errors from crashing the application or losing data silently.

### Benefits

1. **Type Safety**: Guarantees type consistency, reducing runtime errors related to unexpected types.
2. **Automatic Synchronization**: Keeps data consistent across multiple tabs/windows without additional logic.
3. **Graceful Fallbacks and Error Handling**: Ensures robustness against invalid JSON or storage access failures.

### Pros

- **Ease of Use**: Simplifies localStorage interaction within React components.
- **Maintainability**: Centralizes localStorage logic, making future updates easier.
- **Cross-Tab Support**: Automatically synchronizes data across tabs/windows.

### Cons and Potential Issues

1. **Performance Overhead**: Continuous event listening for `storage` events might introduce minor overhead in highly interactive applications with frequent state changes.
2. **Security Concerns**: Storing sensitive information in localStorage can be insecure due to its client-side nature; consider using HTTP-only cookies or server-based storage for sensitive data.
3. **Memory Usage**: Large amounts of data stored in localStorage could lead to increased memory usage, especially on devices with limited resources.

### Conclusion

The `useLocalStorage` hook provides a robust, type-safe mechanism for managing localStorage within React applications. It abstracts away common pitfalls like JSON parsing errors and cross-tab synchronization, making it a valuable utility for developers seeking streamlined state management solutions. However, developers should be mindful of performance implications and security considerations when employing this pattern.

115 t/s, 907 tokens, 8s, 6%
