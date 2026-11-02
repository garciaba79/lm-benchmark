# Ministral 3 8B Instruct 2512
Model: ministral-3-8b-instruct-2512
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

# `useLocalStorage` Hook Implementation

Here's a complete implementation of a type-safe localStorage hook with all the requested features:

```typescript
import { useState, useEffect } from 'react';

function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((val: T) => T)) => void] {
  // State to store our value
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      // Get from localStorage by key
      const item = window.localStorage.getItem(key);
      // Parse stored json or return initialValue
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Return a wrapped version of useState's setter function that ...
  const setValue = (value: T | ((val: T) => T)) => {
    try {
      // Allow value to be a function so we have same API as useState
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;

      // Save state
      setStoredValue(valueToStore);

      // Save to localStorage
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  };

  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === key) {
        try {
          setStoredValue(e.newValue ? JSON.parse(e.newValue) : initialValue);
        } catch (error) {
          console.error(`Error handling storage event for key "${key}":`, error);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key, initialValue]);

  // Sync across tabs/windows
  useEffect(() => {
    const syncWithOtherTabs = () => {
      try {
        const currentValue = JSON.stringify(storedValue);
        window.localStorage.setItem(key, currentValue);
      } catch (error) {
        console.error(`Error syncing with other tabs for key "${key}":`, error);
      }
    };

    // Initial sync
    syncWithOtherTabs();

    // Sync whenever storedValue changes
    const handler = () => syncWithOtherTabs();
    setStoredValue.addEventListener('change', handler);

    return () => {
      setStoredValue.removeEventListener('change', handler);
    };
  }, [key, storedValue]);

  return [storedValue, setValue];
}
```

## Usage Example

```typescript
function MyComponent() {
  const [name, setName] = useLocalStorage<string>('username', 'Guest');

  return (
    <div>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <p>Hello, {name}!</p>
    </div>
  );
}
```

## Benefits

1. **Type Safety**: The hook is fully typed with TypeScript, ensuring type safety for all values stored in localStorage.

2. **Automatic JSON Handling**: Automatically parses JSON when reading and stringifies when writing.

3. **Cross-Tab Syncing**:
   - Uses the `storage` event to detect changes from other tabs/windows
   - Includes a sync mechanism that updates whenever the value changes

4. **Error Handling**: Gracefully handles errors during read/write operations with try-catch blocks.

5. **Cleanup**: Properly removes event listeners on unmount to prevent memory leaks.

6. **Consistent API**: Matches React's `useState` API for easier adoption (`setValue` accepts both values and update functions).

7. **Initial Value Support**: Works with any initial value type, not just strings or primitives.

## Pros

1. **Reusable**: Can be used across multiple components with different keys.
2. **Persistent**: Data persists between page refreshes.
3. **Cross-device**: Syncs across browser tabs/windows (when same domain).
4. **Type-safe**: Prevents type errors at compile time.
5. **No External Dependencies**: Pure React implementation.

## Cons and Potential Issues

1. **Storage Limits**:
   - localStorage has ~5MB limit per origin
   - Large objects may cause performance issues when serializing/deserializing

2. **Security**:
   - All data is stored in plain text (JSON)
   - Vulnerable to XSS attacks if not properly sanitized
   - No encryption by default

3. **Performance**:
   - Frequent small updates might trigger re-renders unnecessarily
   - JSON parsing/stringifying can be expensive for complex objects

4. **Cross-Origin Issues**:
   - The `storage` event only works within the same origin (domain)
   - Doesn't work across different websites or iframes

5. **Initial Load Delay**:
   - First render might show initialValue before localStorage is read
   - Could cause flickering in UI

6. **Complex Objects**:
   - Circular references will break JSON.stringify
   - Functions, class instances, and other non-serializable types won't work

7. **Private Browsing**:
   - Doesn't work in incognito/private browsing modes

## Improved Version (Addressing Some Issues)

Here's an enhanced version that addresses some of the potential issues:

```typescript
function useLocalStorage<T>(
  key: string,
  initialValue: T,
  { serialize = JSON.stringify, deserialize = JSON.parse } = {}
): [T, (value: T | ((val: T) => T)) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? deserialize(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;

      // Validate the value can be serialized
      if (serialize(valueToStore) === undefined) {
        throw new Error('Value cannot be serialized');
      }

      setStoredValue(valueToStore);
      window.localStorage.setItem(key, serialize(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  };

  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === key && e.newValue !== null) {
        try {
          setStoredValue(deserialize(e.newValue));
        } catch (error) {
          console.error(`Error handling storage event for key "${key}":`, error);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key, deserialize]);

  // Sync with other tabs
  useEffect(() => {
    try {
      const currentValue = serialize(storedValue);
      if (currentValue !== null) {
        window.localStorage.setItem(key, currentValue);
      }
    } catch (error) {
      console.error(`Error syncing with other tabs for key "${key}":`, error);
    }
  }, [key, storedValue, serialize]);

  return [storedValue, setValue];
}
```

This improved version:
1. Allows custom serialization/deserialization functions
2. Better handles null values in storage events
3. Adds basic validation before storing
4. More flexible for different data types

## Best Practices When Using This Hook

1. **For complex objects**, consider using a simpler structure or only storing IDs that you can look up elsewhere.

2. **Sanitize inputs** if storing user-generated content to prevent XSS attacks.

3. **Consider size limits** - don't store large amounts of data in localStorage.

4. **Handle edge cases** - provide fallback behavior when localStorage is unavailable.

5. **For sensitive data**, consider using the Web Crypto API for encryption before storing.

6. **Test thoroughly** with:
   - Different browser tabs/windows
   - Private/incognito modes
   - Large objects
   - Network errors

This hook provides a solid foundation for persistent state management in React applications while maintaining type safety and cross-tab synchronization.

114 t/s, 1855 tokens, 16s, 15%
