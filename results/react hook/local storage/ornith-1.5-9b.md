# Ornith 1.5 9B
Model: ornith-1.5-9b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

# useLocalStorage Hook

Here's a production-ready implementation in TypeScript:

```typescript
import { useCallback, useEffect, useState } from 'react';

/** A setter that supports either a new value or an updater function (like setState). */
export type SetValue<T> = (value: T | ((prevValue: T) => T)) => void;

export function useLocalStorage<T>(key: string, initialValue: T): [T, SetValue<T>] {
  // --- Read once on mount -------------------------------------------------
  const readInitial = useCallback(() => {
    try {
      if (typeof window === 'undefined' || !window.localStorage) return initialValue;
      const item = window.localStorage.getItem(key);
      if (item === null) return initialValue;
      // JSON.parse throws on invalid data → fall back to the initial value.
      return JSON.parse(item) as unknown as T;
    } catch (error) {
      console.warn(`[useLocalStorage] Failed to read "${key}":`, error);
      return initialValue;
    }
  }, [key, initialValue]);

  const [storedValue, setStoredValue] = useState(readInitial);

  // --- Re-read when the key changes ---------------------------------------
  useEffect(() => {
    setStoredValue(readInitial());
  }, [readInitial]);

  // --- Write to localStorage (supports functional updates) ----------------
  const setValue: SetValue<T> = useCallback((value) => {
    setStoredValue((prev) => {
      const nextValue = typeof value === 'function' ? (value as (p: T) => T)(prev) : value;
      try {
        if (typeof window === 'undefined' || !window.localStorage) return nextValue;
        // JSON.stringify throws on circular refs / functions → caught below.
        window.localStorage.setItem(key, JSON.stringify(nextValue));
      } catch (error) {
        console.warn(`[useLocalStorage] Failed to write "${key}":`, error);
      }
      return nextValue;
    });
  }, [key]);

  // --- Sync across tabs/windows -------------------------------------------
  useEffect(() => {
    const handleStorageChange = (event: StorageEvent) => {
      if (event.key !== null && event.key !== key) return;
      try {
        const newValue = event.newValue ? JSON.parse(event.newValue) : initialValue;
        setStoredValue(newValue as T);
      } catch (error) {
        console.warn(`[useLocalStorage] Failed to parse "${key}":`, error);
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange); // cleanup on unmount
  }, [key, initialValue]);

  return [storedValue, setValue];
}
```

## Usage

```tsx
// Stringified object — you store/return plain objects, not strings
const [theme, setTheme] = useLocalStorage<string>('app-theme', 'light');

setTheme((prev) => (prev === 'dark' ? 'light' : 'dark')); // functional update

// Number with fallback if nothing is stored yet
const [count, setCount] = useLocalStorage<number>('counter', 0);
```

## How it works

- **Lazy init** — `useState(readInitial)` reads from storage exactly once on mount.
- **Write** — serializes via `JSON.stringify`; the setter mirrors React's `setState` so you can pass an updater function to avoid race conditions between rapid writes.
- **Cross-tab sync** — a `storage` event listener updates other windows/tabs when the key changes. Cleanup removes the listener on unmount (no leaks, no stale updates).
- **Graceful errors** — every `localStorage` access is wrapped in `try/catch`, so corrupted data, quota exhaustion, or security-context failures fall back to `initialValue` instead of crashing your app.

---

## Benefits

1. **Type-safe generics** — call sites get full type inference; no manual casting.
2. **Automatic serialization** — you work with plain objects/numbers/strings, not raw JSON strings.
3. **Robust fallbacks** — stale or corrupted data silently falls back to `initialValue`.
4. **Cross-tab sync for free** — shared settings/state stay in sync across windows of the same origin.
5. **SSR-safe** — guards against `window` being undefined (Next.js / server rendering).
6. **Functional updates** — safe under React 18 StrictMode and rapid successive writes.

## Pros & Cons

| ✅ Pros | ❌ Cons / Limitations |
|---|---|
| Concise `[value, setValue]` API | Can't store **functions**, class instances with methods, or `undefined` values — JSON drops them (e.g. `{a: undefined}` → `{}`). |
| Graceful error handling everywhere | No **deep runtime type validation** — a mismatched stored value passes through as-is; the cast trusts its shape. |
| Handles invalid JSON, quota errors, SSR | **Storage quota** (~5 MB) is exceeded silently (logged). Use IndexedDB for large payloads. |
| Built-in cross-tab sync + cleanup | No automatic **schema migration** — schema changes replace old data with `initialValue`. |
| Zero external dependencies | Security-context access can throw in sandboxed iframes / private modes. |

## Potential issues to be aware of

- **Don't store functions or `undefined`** — they won't survive serialization. Stick to primitives and plain objects.
- **Avoid `undefined` as an initial value** — it round-trips to `null`, breaking the type contract.
- **Storage events only fire on *change*** and only in *other* windows (never your own write), so this hook can't react to values that don't change or updates made locally without a state change.
- **Console noise** — errors are logged via `console.warn`; if storage is frequently corrupted, watch for spam in dev.
- **Type safety caveat** — the cast satisfies the compiler but doesn't guarantee runtime shape matches `T`. If you need strict guarantees (e.g., rejecting a string where an object was expected), add explicit validation before returning the parsed value.

If you'd like, I can show a variant with **deep type checking**, or refactor this into a testable factory pattern for unit testing without rendering.

121 t/s, 9067 tokens, 75s, 56%
