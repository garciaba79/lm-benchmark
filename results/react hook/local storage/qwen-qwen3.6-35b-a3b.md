# Qwen3.6 35B A3B
Model: qwen/qwen3.6-35b-a3b
Test: Hook Local Storage
Created: 11/22/2026, 12:45:28 PM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

I'll create a robust `useLocalStorage` hook that handles all your requirements. Let me break this down into components and explain each part.

## Implementation

```typescript
import { useState, useEffect, useCallback } from 'react';

interface UseLocalStorageReturn<T> {
  value: T;
  setValue: (value: T | ((prevValue: T) => T)) => void;
}

function useLocalStorage<T>(
  key: string,
  initialValue: T
): UseLocalStorageReturn<T> {
  // State to store our value
  // Pass initial state function to useState so logic is only executed once
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      // Get from local storage by key
      const item = window.localStorage.getItem(key);
      // Parse stored JSON or return initialValue
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      // If there's an error parsing, return the initial value
      console.warn(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Return wrapped setValue and state
  const setValue: UseLocalStorageReturn<T>['setValue'] = useCallback(
    (value: T | ((prevValue: T) => T)) => {
      try {
        // Allow value to be a function so we get same behavior as useState
        const valueToStore =
          value instanceof Function ? value(storedValue) : value;
        
        // Save state
        setStoredValue(valueToStore);
        
        // Update localStorage
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
      } catch (error) {
        // Handle potential quota exceeded errors
        console.warn(`Error setting localStorage key "${key}":`, error);
      }
    },
    [key, storedValue]
  );

  // Handle storage events for cross-tab synchronization
  useEffect(() => {
    const handleStorageChange = (event: StorageEvent) => {
      // Check if the event is related to our key
      if (event.key === key && event.newValue !== null) {
        try {
          // Parse the new value from localStorage
          const newValue = JSON.parse(event.newValue);
          setStoredValue(newValue);
        } catch (error) {
          console.warn(`Error parsing storage event for key "${key}":`, error);
        }
      }
    };

    // Add event listener for storage changes
    window.addEventListener('storage', handleStorageChange);

    // Cleanup function to remove event listener
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key]);

  // Sync with localStorage on mount and when initialValue changes
  useEffect(() => {
    try {
      const item = window.localStorage.getItem(key);
      if (item !== null) {
        // Only update if the parsed value is different from initial value
        const parsedValue = JSON.parse(item);
        if (JSON.stringify(parsedValue) !== JSON.stringify(initialValue)) {
          setStoredValue(parsedValue);
        }
      }
    } catch (error) {
      console.warn(`Error initializing localStorage key "${key}":`, error);
    }
  }, [key, initialValue]);

  return { value: storedValue, setValue };
}

export default useLocalStorage;
```

## Usage Examples

### Basic Usage
```tsx
import useLocalStorage from './useLocalStorage';

function App() {
  const [theme, setTheme] = useLocalStorage<string>('theme', 'light');
  
  return (
    <div className={`app ${theme}`}>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </button>
      <p>Current theme: {theme}</p>
    </div>
  );
}
```

### Complex Types
```tsx
interface UserPreferences {
  fontSize: number;
  language: string;
  notifications: boolean;
}

function PreferencesPanel() {
  const [preferences, setPreferences] = useLocalStorage<UserPreferences>(
    'user-preferences',
    {
      fontSize: 16,
      language: 'en',
      notifications: true
    }
  );

  const updateFontSize = (newSize: number) => {
    setPreferences(prev => ({
      ...prev,
      fontSize: newSize
    }));
  };

  return (
    <div>
      <input
        type="range"
        min="12"
        max="24"
        value={preferences.fontSize}
        onChange={(e) => updateFontSize(Number(e.target.value))}
      />
      <p>Font size: {preferences.fontSize}px</p>
    </div>
  );
}
```

### Type-Safe Usage
```tsx
interface AppState {
  currentPage: string;
  sidebarOpen: boolean;
  modalData: { id: number; title: string } | null;
}

function useAppStorage() {
  return useLocalStorage<AppState>('app-state', {
    currentPage: 'home',
    sidebarOpen: false,
    modalData: null
  });
}
```

## Key Features Explained

### 1. **Type Safety**
- Generic type parameter `<T>` ensures type consistency
- TypeScript will catch type mismatches at compile time
- Works with primitive types, objects, arrays, and complex interfaces

### 2. **Automatic JSON Serialization**
- `JSON.stringify()` converts objects to strings for storage
- `JSON.parse()` converts strings back to objects
- Handles both initial values and updates

### 3. **Cross-Tab Synchronization**
- Uses the `storage` event to sync changes across tabs
- Automatically updates state when another tab modifies the same key
- Essential for multi-tab applications

### 4. **Error Handling**
- Graceful handling of JSON parsing errors
- Console warnings for debugging
- Returns initial values on errors to prevent crashes

### 5. **Proper Cleanup**
- Removes event listeners on unmount
- Prevents memory leaks
- Follows React best practices

## Benefits

### ✅ **Pros**
1. **Type Safety**: Full TypeScript support with generics
2. **Persistence**: Data survives page refreshes and browser restarts
3. **Cross-Tab Sync**: Automatic synchronization across browser tabs
4. **Error Resilience**: Handles storage errors gracefully
5. **Functional API**: Follows React patterns with setter functions
6. **No Dependencies**: Pure React implementation
7. **Memory Efficient**: Proper cleanup prevents leaks

### ❌ **Cons**
1. **Storage Limits**: localStorage has ~5-10MB limit per origin
2. **Synchronous API**: Can block main thread with large data
3. **No Expiration**: Data persists indefinitely unless manually removed
4. **Browser Compatibility**: Not available in all environments (SSR, etc.)
5. **Security**: Not suitable for sensitive data (accessible to JavaScript)

## Potential Issues & Solutions

### 1. **Server-Side Rendering (SSR)**
```typescript
// Solution: Check for window availability
if (typeof window !== 'undefined') {
  // Use localStorage
} else {
  // Use memory-only state
}
```

### 2. **Large Data Performance**
```typescript
// Solution: Implement compression or chunking for large datasets
// Or use IndexedDB for larger storage needs
```

### 3. **Storage Quota Exceeded**
```typescript
// Solution: Implement fallback storage or cleanup strategies
try {
  localStorage.setItem(key, JSON.stringify(value));
} catch (error) {
  if (error.name === 'QuotaExceededError') {
    // Implement cleanup or fallback
  }
}
```

### 4. **Initial Value Changes**
The current implementation only syncs on mount. For dynamic initial values:
```typescript
// Add a useEffect to handle initialValue changes
useEffect(() => {
  const item = window.localStorage.getItem(key);
  if (item === null) {
    setStoredValue(initialValue);
  }
}, [key, initialValue]);
```

## Best Practices

1. **Use for non-sensitive data**: Never store passwords or sensitive information
2. **Validate data types**: Ensure parsed data matches expected types
3. **Handle storage limits**: Implement cleanup strategies for large applications
4. **Consider alternatives**: Use IndexedDB for larger datasets
5. **Test thoroughly**: Test across different browsers and storage scenarios

This hook provides a robust, type-safe solution for localStorage management in React applications while addressing common pitfalls and edge cases.

46 t/s, 1900 tokens, 41s, 12%
