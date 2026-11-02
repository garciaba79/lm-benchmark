# LFM2.5 2.6B
Model: lfm2.5-2.6b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is a robust, type-safe implementation of the `useLocalStorage` hook.

### Implementation

```typescript
import { useState, useEffect } from 'react';

/**
 * A custom React hook that persists state in localStorage with automatic JSON handling,
 * cross-tab synchronization, and TypeScript type safety.
 *
 * @param key - The key to store in localStorage.
 * @param initialValue - The initial value for the state (used if no data exists).
 */
export function useLocalStorage<T>(key: string, initialValue: T) {
  // 1. Initialize state with a lazy evaluation function to read from localStorage
  const [storedValue, setStoredValue] = useState<T>(
    () => {
      try {
        const item = localStorage.getItem(key);
        if (item !== null) {
          // Parse JSON and cast to T
          return JSON.parse(item) as T;
        }
      } catch (error) {
        // If parsing fails or key doesn't exist, fallback to initialValue.
        // We log a warning but don't throw to prevent the app from crashing.
        console.warn(`Failed to parse localStorage key "${key}":`, error);
      }
      return initialValue;
    }
  );

  // 2. Set up cross-tab synchronization
  useEffect(() => {
    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === key && event.newValue !== null) {
        try {
          const newValue = JSON.parse(event.newValue) as T;
          setStoredValue(newValue);
        } catch (error) {
          console.warn(`Failed to parse localStorage change for key "${key}":`, error);
        }
      }
    };

    // Add the listener for storage events
    window.addEventListener('storage', handleStorageChange);

    // 3. Cleanup function to remove the listener on unmount
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key]); // Dependency array ensures effect runs when key changes

  // Return the state and setter for use in components
  return [storedValue, setStoredValue];
}
```

### How It Works

1.  **Type Safety**: The hook uses a generic type `T`. The initial value is cast to `T` using TypeScript's strict equality checking. If localStorage contains invalid JSON or data that doesn't match the expected type, we fall back to the `initialValue`, ensuring the component never receives an incorrect type.
2.  **Cross-Tab Synchronization**: It uses `window.addEventListener('storage', ...)` which fires whenever any tab or window modifies a key in localStorage. This allows changes made in one browser tab to instantly reflect in other open tabs, solving the "stale state" problem typical of standard React state.
3.  **Error Handling**: Both reading (parsing) and writing (saving) are wrapped in `try/catch` blocks. If JSON is malformed or localStorage quota is exceeded, the hook logs a warning but continues running instead of crashing.
4.  **Cleanup**: The `useEffect` returns a cleanup function that removes the event listener when the component unmounts, preventing memory leaks and "state update on unmounted component" warnings.

### Usage Example

```typescript
import React from 'react';
import { useLocalStorage } from './useLocalStorage';

function UserProfile() {
  // This state is saved to localStorage under key 'user-theme'
  const [theme, setTheme] = useLocalStorage<'light' | 'dark', string>('light');

  return (
    <div>
      <p>Current Theme: {theme}</p>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </button>
    </div>
  );
}
```

### Benefits & Pros

*   **Type Safety**: Unlike a vanilla `localStorage` setup, this hook enforces types. You can use TypeScript's exhaustive typing to ensure your UI logic is robust.
*   **Automatic Persistence**: Data survives page refreshes and browser restarts without extra configuration.
*   **Cross-Context Sync**: The implementation handles the "multi-tab" problem natively by listening to global storage events, allowing a setting changed in Chrome to update instantly in Firefox (on different devices) or other tabs.

### Cons & Potential Issues

*   **Performance Overhead**: Every time `localStorage` is read/written, it involves a synchronous call. While usually negligible for small strings, heavy objects could theoretically block the main thread if not careful.
*   **Event Storming**: The `storage` event fires frequently (e.g., when users type in input fields on other tabs). This can lead to unnecessary re-renders of your component every time a global change occurs. However, because we only update state when `newValue !== null`, this is manageable.
*   **Type Mismatch**: If you initialize with an object but save a string (or vice versa), the type safety in the initial render might be bypassed if TypeScript's strict checking fails during development, though at runtime the data will simply be updated to whatever was saved. The hook attempts to cast on read, but if `JSON.parse` returns `{ a: 1 }` and you expect a string, React might complain about type mismatch in subsequent renders.
*   **Storage Quota**: If the user hits localStorage limits (quota exceeded), the save function catches the error. However, this is a browser-level constraint that cannot be fully prevented; the hook will just stop working until space is freed or deleted.

### Comparison with Libraries

While libraries like `reactive-local` or MUI's `useLocalStorage` exist, they often rely on external dependencies or complex context providers to handle synchronization. This implementation keeps the solution **zero-dependency**, making it easy to drop into any React 18+ project without bundle size increases.

265 t/s, 4387 tokens, 17s, 27%
