# Qwen3.8 27B
Model: qwen/qwen3.8-27b
Test: Hook Local Storage
Created: 11/03/2026, 02:24:29 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

```typescript
import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * A React hook that syncs state with localStorage.
 *
 * @param key - The localStorage key
 * @param initialValue - The initial value if nothing is stored
 * @returns [state, setState] tuple similar to useState
 */
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((prev: T) => T)) => void] {
  // Read from localStorage, parse JSON, fall back to initialValue
  const readFromStorage = useCallback((): T => {
    try {
      const item = window.localStorage.getItem(key);
      return item !== null ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      // JSON parse error or access denied – return initial value
      console.warn(`useLocalStorage: Error reading key "${key}":`, error);
      return initialValue;
    }
  }, [key, initialValue]);

  // Initial state: read from storage
  const [storedValue, setStoredValue] = useState<T>(() => readFromStorage());

  // Update state and write to localStorage
  const setValue: (value: T | ((prev: T) => T)) => void = useCallback(
    (value) => {
      setStoredValue((prev) => {
        // If function updater, resolve it
        const newValue =
          typeof value === 'function'
            ? (value as (prev: T) => T)(prev)
            : value;

        try {
          window.localStorage.setItem(key, JSON.stringify(newValue));
        } catch (error) {
          // Quota exceeded, access denied, etc.
          console.warn(`useLocalStorage: Error writing key "${key}":`, error);
        }

        return newValue;
      });
    },
    [key]
  );

  // Listen for 'storage' events to sync across tabs/windows
  useEffect(() => {
    const handleStorageChange = (event: StorageEvent) => {
      // Only react if the event is for our key
      if (event.key !== key) return;

      // If the value was cleared (newValue is null), reset to initial
      if (event.newValue === null) {
        setStoredValue(initialValue);
        return;
      }

      try {
        const parsedValue = JSON.parse(event.newValue) as T;
        setStoredValue(parsedValue);
      } catch (error) {
        console.warn(`useLocalStorage: Error parsing storage event for key "${key}":`, error);
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [key, initialValue]);

  // Clean up: remove the key from localStorage on unmount if desired?
  // Typically we don't remove on unmount because other components may still use it.
  // Instead, we just ensure we've removed listeners (done above).
  // No additional cleanup needed for the key itself.

  return [storedValue, setValue];
}

export default useLocalStorage;
```

## Explanation of the Implementation

### How It Works

1. **Initial Read**: On first render, `readFromStorage` reads the value from `localStorage` using `getItem`, parses it with `JSON.parse`, and falls back to `initialValue` if the key doesn't exist or parsing fails.

2. **Setting Values**: `setValue` accepts either a direct value or a function updater (like `useState`). It updates React state and writes the new value to `localStorage` via `setItem` with `JSON.stringify`.

3. **Cross-Tab Sync**: A `storage` event listener is registered. When another tab/window modifies the same key, the `storage` event fires in *other* tabs (not the one that made the change). The listener parses the new value and updates the local state.

4. **Error Handling**: All `localStorage` operations are wrapped in try/catch blocks to handle:
   - `QuotaExceededError` (storage full)
   - Access denied (e.g., privacy mode restrictions)
   - JSON parse errors (malformed data)
   - Any other runtime errors

5. **Cleanup**: The `useEffect` returns a cleanup function that removes the `storage` event listener on unmount, preventing memory leaks.

### Type Safety

- The hook is generic over `T`, so `state` is typed as `T` and `setValue` accepts `T` or `(prev: T) => T`.
- `JSON.parse` returns `any`, so we cast to `T` after parsing. This is a trade-off for simplicity; in production, you might want runtime validation (e.g., with Zod) to ensure the parsed value matches `T`.

### Benefits

| Benefit | Description |
|---|---|
| **Persistence** | State survives page reloads and browser restarts. |
| **Cross-tab sync** | Changes in one tab are reflected in others automatically. |
| **Type safety** | Generic typing ensures compile-time checks for the value type. |
| **Familiar API** | Mimics `useState`, making it easy to adopt. |
| **Graceful degradation** | Errors are caught and logged; the app doesn't crash. |
| **No external dependencies** | Pure React + browser APIs. |

### Pros

- Simple to use: `const [count, setCount] = useLocalStorage<number>('count', 0);`
- Works seamlessly with functional components and hooks.
- Supports function updaters, enabling atomic updates like `setCount((c) => c + 1)`.
- Cross-tab synchronization is automatic and event-driven.
- Error handling prevents crashes from quota issues or malformed data.

### Cons

| Con | Details |
|---|---|
| **No runtime validation** | `JSON.parse` returns `any`; if stored data doesn't match `T`, you'll get runtime errors. Consider adding a validator. |
| **Limited storage size** | `localStorage` is typically capped at ~5–10 MB. Large objects will fail. |
| **Synchronous API** | `localStorage` is synchronous, which can block the main thread for large writes. |
| **Privacy mode issues** | Some browsers (especially in private/incognito mode) restrict or disable `localStorage`, causing errors. |
| **No encryption** | Data is stored in plain text. Avoid storing sensitive information. |
| **Key collisions** | If multiple unrelated features use the same key, they'll overwrite each other. |
| **No built-in debouncing** | Frequent updates (e.g., on every keystroke) will write to `localStorage` every time, which can be expensive. |

### Potential Issues & Mitigations

1. **Stale closures with `initialValue`**: If `initialValue` is an object/array created inline, it changes identity on every render, causing the `useEffect` to re-run unnecessarily. **Mitigation**: Pass a stable reference or use a factory function for the initial value.

2. **Race conditions across tabs**: If two tabs update the same key rapidly, the last write wins. There's no conflict resolution. **Mitigation**: For critical data, implement optimistic concurrency control (e.g., version numbers).

3. **Large values**: Writing large objects to `localStorage` can be slow and hit quota limits. **Mitigation**: Only store small, serializable data. For larger data, consider `IndexedDB` with an async wrapper.

4. **Serialization edge cases**: `Date`, `Map`, `Set`, `undefined`, functions, and circular references don't serialize/deserialize correctly with `JSON.stringify`/`parse`. **Mitigation**: Use custom serializers or avoid storing such types.

5. **SSR compatibility**: `window` and `localStorage` don't exist in server-side rendering. **Mitigation**: Guard with `typeof window !== 'undefined'` if used in an SSR environment (e.g., Next.js).

### Example Usage

```tsx
import { useLocalStorage } from './useLocalStorage';

function Counter() {
  const [count, setCount] = useLocalStorage<number>('my-counter', 0);

  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

This hook provides a clean, type-safe way to persist React state in `localStorage` with automatic cross-tab synchronization and robust error handling.

17 t/s, 1891 tokens, 110s
