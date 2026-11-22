# Qwen3.5 9B The Defiant Fable Uncnr Heretic NEO MAX
Model: qwen3.5-9b-the-defiant-fable-uncensored-heretic-neo-imatrix-max-mtp
Test: Hook Local Storage
Created: 11/22/2026, 02:55:26 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here’s a production-ready `useLocalStorage` hook in TypeScript using React 18+ patterns, with cross-tab sync via BroadcastChannel (no external libs), graceful error handling, cleanup on unmount, and proper JSON serialization.

```ts
import { useEffect, useRef, useState } from 'react';

type StorageEvent<T> = Event & {
  detail: string; // serialized value
};

/**
 * useLocalStorage<T>(key, initialValue)
 *
 * - Reads/writes localStorage with automatic JSON stringify/parse.
 * - Type-safe via generics (T).
 * - Syncs across tabs/windows using BroadcastChannel + StorageEvent listener.
 * - Gracefully handles errors and stale data.
 * - Cleans up listeners on unmount.
 */
export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((prev: T) => T)) => void] {
  // State holds the current value
  const [state, setState] = useState<T>(() => {
    try {
      if (!window || !localStorage) return initialValue;

      const item = localStorage.getItem(key);
      if (item === null) return initialValue;

      // Safe JSON parse with fallback to initial value on failure
      return JSON.parse(item) as T;
    } catch {
      return initialValue;
    }
  });

  // Refs for stable references across renders
  const keyRef = useRef(key);
  const isMountedRef = useRef(false);
  const channelRef = useRef<BroadcastChannel | null>(null);

  // Ensure we always use the latest key
  useEffect(() => {
    if (!window || !localStorage) return;

    // Initialize BroadcastChannel for cross-tab sync
    try {
      channelRef.current = new BroadcastChannel(`useLocalStorage_${key}`);
    } catch (err) {
      console.warn('BroadcastChannel not supported:', err);
    }

    // Listen to storage events from other tabs/windows
    const handleStorageEvent = (e: StorageEvent<T>) => {
      if (!window || !localStorage) return;

      // Ignore our own writes (same origin, same tab)
      if (e.source === window && e.detail !== undefined) {
        try {
          const parsed = JSON.parse(e.detail);
          setState(parsed as T);
        } catch {
          // If parsing fails, ignore the event to avoid corrupting state
          return;
        }
      }
    };

    window.addEventListener('storage', handleStorageEvent as EventListener);

    // Listen for messages from other tabs using BroadcastChannel
    if (channelRef.current) {
      channelRef.current.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          setState(parsed as T);
        } catch {
          console.warn('Failed to parse cross-tab sync message:', event.data);
        }
      };
    }

    isMountedRef.current = true;

    return () => {
      // Cleanup listeners on unmount
      window.removeEventListener('storage', handleStorageEvent as EventListener);

      if (channelRef.current) {
        channelRef.current.onmessage = null;
        channelRef.current.close();
      }

      isMountedRef.current = false;
    };
  }, []); // Run once on mount

  // Sync effect: write to localStorage and broadcast when state changes
  useEffect(() => {
    if (!isMountedRef.current) return;

    const currentKey = keyRef.current;
    try {
      const serialized = JSON.stringify(state);

      // Write to localStorage (triggers storage event in other tabs)
      localStorage.setItem(currentKey, serialized);

      // Broadcast to other tabs using BroadcastChannel for faster sync
      if (channelRef.current && typeof state === 'object' && state !== null) {
        channelRef.current.postMessage(serialized);
      }
    } catch (err) {
      console.error('Failed to write localStorage:', err);
    }
  }, [state]);

  // Update key reference when the dependency changes
  useEffect(() => {
    keyRef.current = key;
  }, [key]);

  return [state, setState];
}
```

### How It Works (Brief)

- **State & Initialization**: On mount, it safely reads from localStorage and falls back to `initialValue` if missing or malformed.
- **Write & Sync**: When the value changes:
  - Serializes with JSON.stringify.
  - Writes to localStorage (native cross-tab sync via StorageEvent).
  - Sends a message via BroadcastChannel for faster, direct tab-to-tab updates.
- **Cross-Tab Listening**:
  - `storage` event listener catches writes from other tabs/windows.
  - BroadcastChannel’s `onmessage` handler receives messages directly.
- **Cleanup**: On unmount:
  - Removes the storage listener.
  - Closes and nullifies the BroadcastChannel.
- **Type Safety**: Generic `<T>` ensures TypeScript knows the shape of stored data.

---

### Benefits

- **Type-safe**: Compile-time checks for your data structure via generics.
- **Zero dependencies**: Pure React + browser APIs; works in SSR-friendly setups if guarded (e.g., `if (!window)`).
- **Cross-tab sync**: Keeps all tabs/windows in lockstep without extra state management.
- **Graceful error handling**: Catches JSON errors, missing localStorage, and unsupported BroadcastChannel environments.
- **Clean lifecycle**: Properly unregisters listeners to avoid memory leaks or stale callbacks.

---

### Pros & Cons / Potential Issues

**Pros:**
- Simple API: `[value, setValue]` like React state.
- Automatic serialization; no manual stringify/parse needed in components.
- Works with complex objects (arrays, nested structures) as long as they’re JSON-serializable.

**Cons:**
- **JSON-only**: Non-stringifiable types (functions, Dates without conversion, Symbols, etc.) will fail or lose data. Convert them before storing if needed.
- **Size limits**: localStorage is typically 5–10 MB per origin; large payloads can cause quota errors or slow writes.
- **Security model**: Data persists across sessions and is accessible to any script on the same origin (or via service workers). Don’t store sensitive tokens without encryption.
- **SSR/Server-side rendering**: On the server, `window`/`localStorage` may be undefined; guard with checks or provide a fallback initial value.

**Potential Issues & Mitigations:**
1. **Race conditions on mount**: If multiple components initialize from localStorage concurrently, they’ll all read the same snapshot. This is usually fine for simple app state but can cause flicker in complex scenarios. Consider using a single “store” component or context if you need stricter consistency.
2. **BroadcastChannel not supported**: In very old browsers (e.g., IE), it falls back to localStorage-only sync, which still works but slightly slower. You can detect and warn: `if (!('BroadcastChannel' in window)) console.warn('BroadcastChannel unsupported; relying on StorageEvent only.');`
3. **Stale closures**: The hook uses refs (`keyRef`, `isMountedRef`) so effects always see the latest values without causing re-renders for ref updates. This is a standard React 18 pattern and avoids stale closure bugs.

---

### Example Usage

```tsx
import { useLocalStorage } from './useLocalStorage';

function Counter() {
  const [count, setCount] = useLocalStorage<number>('counter', 0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}

function App() {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('app-theme', 'light');

  return (
    <>
      <h1>{theme === 'dark' ? 'Dark Mode' : 'Light Mode'}</h1>
      <Counter />
    </>
  );
}
```

This hook gives you a robust, type-safe localStorage abstraction that syncs across tabs and cleans up properly on unmount.

105 t/s, 1804 tokens, 17s, 12%
