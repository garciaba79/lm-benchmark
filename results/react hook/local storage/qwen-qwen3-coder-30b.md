# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: Hook Local Storage
Created: 11/03/2026, 02:58:08 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

```typescript
import { useState, useEffect, useCallback } from 'react';

function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  // Get initial value from localStorage or fallback to provided initialValue
  const getStoredValue = useCallback((): T => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  }, [key, initialValue]);

  // State to store our value
  const [storedValue, setStoredValue] = useState<T>(getStoredValue);

  // Update localStorage when state changes
  const setValue = useCallback((value: T) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key]);

  // Handle storage events from other tabs/windows
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === key) {
        try {
          const newValue = e.newValue ? JSON.parse(e.newValue) : initialValue;
          setStoredValue(newValue);
        } catch (error) {
          console.error(`Error parsing localStorage change for key "${key}":`, error);
        }
      }
    };

    // Add event listener
    window.addEventListener('storage', handleStorageChange);

    // Cleanup function to remove event listener
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key, initialValue]);

  // Cleanup effect for when component unmounts
  useEffect(() => {
    return () => {
      // No specific cleanup needed for this hook
      // Storage event listeners are removed in the previous cleanup
    };
  }, []);

  return [storedValue, setValue];
}

export default useLocalStorage;
```

## Benefits

1. **Type Safety**: Generic type parameter `T` ensures compile-time type checking
2. **Automatic Serialization**: Handles JSON parsing/stringifying automatically
3. **Cross-tab Synchronization**: Automatically syncs changes across browser tabs/windows
4. **Error Handling**: Gracefully handles localStorage errors without crashing
5. **React 18+ Compatible**: Uses modern React hooks patterns
6. **Memory Efficient**: Only stores the current value in state, not the entire localStorage

## Pros

- **Easy to Use**: Simple API - just pass key and initial value
- **No External Dependencies**: Pure React implementation
- **Automatic Sync**: Changes in one tab are immediately visible in others
- **Robust Error Handling**: Catches and logs errors without breaking the app
- **Clean Cleanup**: Properly removes event listeners on unmount
- **Performance**: Uses `useCallback` to prevent unnecessary re-renders

## Cons

1. **Limited Storage**: localStorage has ~5-10MB limit per domain
2. **Blocking Operations**: localStorage operations block the main thread
3. **No Encryption**: Data is stored in plain text (security concern)
4. **Browser Limitations**: Not available in private browsing modes or when disabled
5. **Sync Issues**: Potential race conditions in high-concurrency scenarios
6. **No Expiration**: No built-in way to automatically expire data

## Potential Issues

1. **Storage Quota Exceeded**: Large objects can cause `QuotaExceededError`
2. **Security Restrictions**: Some browsers block localStorage in private mode
3. **Performance Impact**: Large JSON parsing/serialization can be slow
4. **Type Inference**: Complex nested types might not infer correctly
5. **SSR Compatibility**: Won't work on server-side rendering (use with caution)
6. **Data Corruption**: Malformed JSON in localStorage can cause parsing errors
7. **Event Listener Memory Leaks**: Though we clean up, multiple hooks could theoretically create issues

## Usage Example

```typescript
// Simple string value
const [name, setName] = useLocalStorage<string>('userName', 'John');

// Object value
const [user, setUser] = useLocalStorage<{ name: string; age: number }>(
  'userData', 
  { name: '', age: 0 }
);

// Array value
const [items, setItems] = useLocalStorage<string[]>('shoppingList', []);

// Number value
const [count, setCount] = useLocalStorage<number>('counter', 0);
```

This hook provides a solid foundation for localStorage management with proper error handling and cross-tab synchronization while maintaining type safety and React best practices.

61 t/s, 976 tokens, 16s
