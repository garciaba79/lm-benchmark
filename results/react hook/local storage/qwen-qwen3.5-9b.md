# Qwen3.5 9B
Model: qwen/qwen3.5-9b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

# `useLocalStorage` Hook in TypeScript

This React 18+ hook provides a safe, typed interface for persisting and syncing data using the browser's `localStorage`. It handles JSON serialization/deserialization automatically, includes cleanup logic on unmount, gracefully manages errors, and supports event-based cross-tab synchronization.

---

## Implementation

```ts
import { useEffect, useCallback, useState } from 'react';
import type { DependencyList } from 'react';

export interface UseLocalStorageOptions<T> {
  defaultValue: T;
}

type UseLocalStorageReturn<T> = [T, (value: T) => void];

export function useLocalStorage<T>(
  key: string,
  defaultValue?: T
): UseLocalStorageReturn<T> {
  const initialValue = defaultValue ?? getDefaultFromStorage(key);

  const [value, setValue] = useState<T>(() => {
    try {
      const storedValue = getStoredValue(key);
      return storedValue !== null ? storedValue : initialValue;
    } catch {
      console.warn(`Failed to retrieve value from localStorage: ${key}`);
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      setValue(value);
    } catch {
      console.error('Failed to store value in localStorage');
    }
  }, [value]);

  const set = useCallback(
    (newValue: T) => {
      try {
        localStorage.setItem(key, JSON.stringify(newValue));
      } catch (err) {
        console.error(`Failed to set value for ${key}:`, err);
      }
    },
    [key]
  );

  useEffect(() => {
    const handler = (event: StorageEvent) => {
      if (event.key === key && event.newValue !== null) {
        try {
          setValue(JSON.parse(event.newValue));
        } catch {
          console.error(`Failed to parse stored value for ${key}`);
        }
      }
    };

    window.addEventListener('storage', handler);

    return () => window.removeEventListener('storage', handler);
  }, [key]);

  return [value, set];
}

function getStoredValue<T>(key: string): T | null {
  try {
    const item = localStorage.getItem(key);
    if (!item) return null;
    return JSON.parse(item);
  } catch {
    console.warn(`Failed to parse stored value for ${key}`);
    return null;
  }
}

function getDefaultFromStorage<T>(key: string): T {
  try {
    const item = localStorage.getItem(key);
    if (!item) throw new Error('Default value required');
    return JSON.parse(item) as T;
  } catch {
    console.warn(`Failed to retrieve default from storage for ${key}`);
    throw new Error(`Provide a default value for key: ${key}`);
  }
}
```

---

## Key Features

- **Type Safety:** Fully typed with generic `T`, inferred from the initial/default value.
- **JSON Handling:** Automatically handles stringify/parse on store/retrieve.
- **Error Resilience:** Catches JSON or storage errors and logs them safely.
- **Cleanup:** Removes event listeners when component unmounts.
- **Cross-tab Sync:** Leverages `window.addEventListener('storage', ...)` to respond to external changes.

> ⚠️ Note: This hook does **not** sync data automatically when the component in one tab updates. That's by design—localStorage only emits events when another **tab/window** modifies storage, not during same-origin local writes. If you want true bidirectional syncing across tabs, implement it with an external event bus or a Service Worker (advanced).

---

## Usage Example

```ts
function UserSettings() {
  const [theme, setTheme] = useLocalStorage<'dark' | 'light'>('app-theme', 'light');
  const [user, setUser] = useLocalStorage<User | null>('currentUser', null);

  return (
    <div>
      <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
        Toggle Theme: {theme}
      </button>
      <pre>{JSON.stringify(user, null, 2)}</pre>
    </div>
  );
}
```

---

## Benefits & Pros/Cons

### ✅ Benefits / Pros

- **Type-safe and reusable:** Strong typing prevents runtime errors.
- **Automatic JSON handling:** No boilerplate serialization logic needed.
- **Cross-tab synchronization:** Works for read-only events triggered externally.
- **Cleanup on unmount:** Prevents memory leaks or event listener buildup.
- **Error-resilient:** Gracefully degrades on storage failures.

### ❌ Cons / Issues

- **Not safe for sensitive data:** Avoid storing passwords, tokens, etc.
- **Same-tab updates do NOT trigger listeners:** `localStorage.setItem` only emits events in different tabs/windows.
- **Large payloads may break quota:** localStorage has a ~5MB limit.
- **Limited to simple structures:** JSON cannot hold functions or complex objects with circular references.

---

## Potential Pitfalls & Solutions

| Issue | Solution |
|-------|----------|
| No cross-tab sync on same origin updates | Use `localStorage` only for external triggers; use `BroadcastChannel`, `SharedArrayBuffer`, or a message broker for real-time sync |
| JSON parse failures | Always wrap in `try/catch` and return defaults or null |
| Quota exceeded errors | Implement data compression, pagination, or backend fallback |
| Storage not supported (e.g., server-rendered) | Fallback gracefully; show toast or alert on initial load |

---

## Recommended Alternatives for Production

- **React Context + Server State:** For app-wide state, prefer server-driven updates.
- **Zustand / Jotai:** For client-only state with built-in persistence.
- **IndexedDB:** For larger datasets beyond localStorage limits.
- **Service Worker or BroadcastChannel:** For advanced cross-tab event synchronization.

---

## Final Thoughts

The `useLocalStorage` hook is ideal for persisting simple app state (themes, toggles, preferences) in a typed and safe way. While not capable of bidirectional real-time syncing on its own, it's an excellent foundation when combined with other tools like BroadcastChannel or backend APIs for more complex sync scenarios.

110 t/s, 1610 tokens, 15s, 10%
