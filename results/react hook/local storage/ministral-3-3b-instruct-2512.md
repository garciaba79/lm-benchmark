# Ministral 3 3B Instruct 2512
Model: ministral-3-3b-instruct-2512
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

# `useLocalStorage<T>` Hook in React

Here's a comprehensive implementation of a type-safe localStorage hook with automatic sync across tabs/windows:

```typescript
import { useState, useEffect } from 'react';

type UseLocalStorageOptions = {
  shouldSync?: boolean;
};

export function useLocalStorage<T>(key: string, initialValue: T, options: UseLocalStorageOptions = {}): [T | null, (value: T) => void] {
  const { shouldSync = true } = options;

  // Parse stored value if it exists
  const getItem = () => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Failed to parse localStorage item ${key}:`, error);
      return initialValue;
    }
  };

  // Current state
  const [storedValue, setStoredValue] = useState<T | null>(getItem);

  // Sync with storage when value changes
  useEffect(() => {
    if (shouldSync) {
      try {
        window.localStorage.setItem(key, JSON.stringify(storedValue));
      } catch (error) {
        console.error(`Failed to save localStorage item ${key}:`, error);
      }
    }
  }, [storedValue, key, shouldSync]);

  // Sync across tabs/windows if enabled
  useEffect(() => {
    const handleStorageChange = () => {
      try {
        const newValue = getItem();
        setStoredValue(newValue);
      } catch (error) {
        console.error(`Failed to sync localStorage item ${key}:`, error);
      }
    };

    if (shouldSync && window.addEventListener) {
      window.addEventListener('storage', handleStorageChange);
    }

    return () => {
      if (shouldSync && window.removeEventListener) {
        window.removeEventListener('storage', handleStorageChange);
      }
    };
  }, [key, shouldSync]);

  // Return both the stored value and a function to update it
  const setValue = (value: T | ((prev: T) => T)) => {
    try {
      setStoredValue(value instanceof Function ? value(storedValue) : value);
    } catch (error) {
      console.error(`Failed to update localStorage item ${key}:`, error);
      // Fallback to initial value if update fails
      setStoredValue(initialValue);
    }
  };

  return [storedValue, setValue];
}
```

## Benefits and Pros

1. **Type Safety**: Uses TypeScript generics to ensure type safety when storing complex objects.
2. **Automatic Sync**: Automatically syncs data across tabs/windows when enabled.
3. **Error Handling**: Gracefully handles parsing and storage errors with try-catch blocks.
4. **Cleanup**: Properly removes event listeners on unmount.
5. **Flexible Updates**: Supports both direct values and update functions (like Redux's `update` pattern).
6. **No External Dependencies**: Pure React implementation without any libraries.

## Potential Issues and Considerations

1. **Browser Compatibility**:
   - Works in all modern browsers but may have limited support in very old ones
   - Some edge cases with very large objects (localStorage has a 5MB limit)

2. **Performance Impact**:
   - The storage event listener adds minimal overhead but could impact performance in heavy applications
   - Each write operation triggers both the state update and storage sync

3. **Security Concerns**:
   - LocalStorage is accessible to all tabs/windows on the same domain
   - Sensitive data should be handled carefully (consider encryption for sensitive info)

4. **Race Conditions**:
   - If multiple tabs modify the same key simultaneously, there might be race conditions
   - The hook doesn't implement optimistic updates or conflict resolution

5. **Memory Leaks**:
   - While cleanup is implemented, very large datasets could cause memory issues
   - The storage event listener could potentially leak if not properly cleaned up

## Usage Example

```typescript
function UserProfile() {
  const [name, setName] = useLocalStorage<string>('userName', 'John Doe');
  const [age, setAge] = useLocalStorage<number>('userAge', 30);

  return (
    <div>
      <h1>Welcome {name}</h1>
      <p>You are {age} years old</p>

      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <input
        type="number"
        value={age}
        onChange={(e) => setAge(Number(e.target.value))}
      />
    </div>
  );
}
```

## Advanced Usage with Sync Control

```typescript
function App() {
  const [data, setData] = useLocalStorage('appState', { count: 0 }, {
    shouldSync: false // Disable sync for this component
  });

  return (
    <button onClick={() => setData(prev => ({...prev, count: prev.count + 1})}>
      Increment (local only)
    </button>
  );
}
```

This implementation provides a robust foundation that can be extended with additional features like debouncing writes or more sophisticated conflict resolution if needed.

216 t/s, 1125 tokens, 5s, 11%
