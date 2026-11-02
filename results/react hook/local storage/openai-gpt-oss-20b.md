# GPT-OSS 20B
Model: openai/gpt-oss-20b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

## `useLocalStorage` – a fully‑typed, sync‑aware wrapper around the browser’s `localStorage`

```tsx
import { useState, useEffect } from "react";

/**
 * Hook that keeps a value in sync with localStorage.
 *
 * @param key          The key under which the value is stored.
 * @param initialValue A fallback value (used on first load or if the key is missing).
 * @returns [value, setValue]
 */
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, React.Dispatch<React.SetStateAction<T>>] {
  /* ------------------------------------------------------------ *
   * 1️⃣ Read the value from localStorage once during component   *
   *    initialization. If parsing fails we fall back to          *
   *    `initialValue`.                                            *
   * ------------------------------------------------------------ */
  const readValue = (): T => {
    if (typeof window === "undefined") return initialValue; // SSR guard

    try {
      const storedValue = window.localStorage.getItem(key);
      if (storedValue === null) return initialValue;

      // JSON.parse may throw – we catch it and treat as “missing”
      return JSON.parse(storedValue) as T;
    } catch (_) {
      console.warn(`useLocalStorage: Unable to read key "${key}" from localStorage`);
      return initialValue;
    }
  };

  /* ------------------------------------------------------------ *
   * 2️⃣ Create a state that mirrors the stored value.            *
   * ------------------------------------------------------------ */
  const [storedValue, setStoredValue] = useState<T>(readValue);

  /* ------------------------------------------------------------ *
   * 3️⃣ Persist changes to localStorage whenever `storedValue`   *
   *    changes.                                                  *
   * ------------------------------------------------------------ */
  useEffect(() => {
    if (typeof window === "undefined") return;

    try {
      const valueToStore = storedValue === undefined ? null : storedValue;
      if (valueToStore === null) {
        window.localStorage.removeItem(key);
      } else {
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
      }
    } catch (error) {
      console.warn(`useLocalStorage: Unable to write key "${key}"`, error);
    }
  }, [key, storedValue]);

  /* ------------------------------------------------------------ *
   * 4️⃣ Sync across tabs/windows via the `storage` event.       *
   *    The callback runs only when another tab changes the same  *
   *    key – we read it again and update our state.             *
   * ------------------------------------------------------------ */
  useEffect(() => {
    if (typeof window === "undefined") return;

    const handleStorage = (event: StorageEvent) => {
      // Only react to changes on the key we care about
      if (event.key !== key) return;
      setStoredValue(readValue());
    };

    window.addEventListener("storage", handleStorage);
    // Cleanup on unmount
    return () => window.removeEventListener("storage", handleStorage);
  }, [key]);

  /* ------------------------------------------------------------ *
   * 5️⃣ Return the state and a setter that works like          *
   *    React's `setState`. The setter accepts either a value or a     *
   *    function `(prev) => newVal`, just like `useState`.           *
   * ------------------------------------------------------------ */
  const setValue: React.Dispatch<React.SetStateAction<T>> = (value) => {
    try {
      // Allow functional updates
      const valueToStore =
        typeof value === "function"
          ? (value as Function)(storedValue)
          : value;

      setStoredValue(valueToStore);
      // Persist immediately – the effect above will also run,
      // but this guarantees sync even if the effect is delayed.
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.warn(`useLocalStorage: Unable to set key "${key}"`, error);
    }
  };

  return [storedValue, setValue];
}
```

### How to use it

```tsx
import { useLocalStorage } from "./useLocalStorage";

export function Counter() {
  const [count, setCount] = useLocalStorage<number>("counter", 0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>+</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

---

## What the hook does

| Feature | Implementation |
|---------|----------------|
| **Type safety** | Generic `T` keeps your value typed. |
| **JSON (de)serialization** | Automatically stringifies when writing, parses when reading. |
| **SSR guard** | Works in environments without `window`. |
| **Error handling** | Catches JSON parse/write errors and falls back to a default value or logs warnings. |
| **Cross‑tab sync** | Listens for the browser’s `storage` event. |
| **Cleanup** | Removes the `storage` listener on unmount. |

---

## Benefits

1. **Zero boilerplate** – just call the hook, no manual serialization code.
2. **Type safety** – TypeScript guarantees that you read/write values of the same type.
3. **Consistency across tabs** – All open windows stay in sync automatically.
4. **Graceful degradation** – If localStorage is unavailable (e.g., in Safari’s private mode) or corrupted, the hook falls back to `initialValue` and logs a warning instead of crashing.
5. **Simplicity** – No external dependencies; pure React + TypeScript.

---

## Pros & Cons

| ✅ Pros | ⚠️ Cons |
|---------|--------|
| **Declarative** – Works like `useState`, making it intuitive for React devs. | **Performance** – Serializing large objects on every state change can be expensive. Use the hook only for lightweight data or add a debounce if needed. |
| **Sync‑aware** – Keeps tabs/windows consistent without extra plumbing. | **Storage quota** – Browsers limit localStorage (~5 MB). Exceeding it throws silently; you’ll see warnings in console. |
| **SSR friendly** – Guards against `window` being undefined. | **No encryption** – Data is stored as plain JSON; don't store secrets. |
| **Error‑tolerant** – Catches and logs errors instead of throwing. | **Race conditions** – If two tabs write simultaneously, the last one wins; you may need a merge strategy for complex data. |

---

## Potential Issues & Mitigations

1. **Large values / frequent updates**  
   *Mitigation*: Store only minimal data or use `useRef` to batch writes.

2. **Concurrent tab writes**  
   *Mitigation*: Add optimistic locking (e.g., store a version number) or merge changes manually.

3. **Private/Incognito mode restrictions**  
   *Mitigation*: Detect errors on write and fall back to in‑memory state (`useState` only).

4. **Non‑JSON serializable values**  
   *Mitigation*: The hook expects `T` to be JSON‑serializable; avoid functions, Dates, Maps unless you transform them.

5. **Cleanup timing**  
   *Mitigation*: The listener is removed in the cleanup function of the effect that adds it, so there’s no memory leak.

---

## Summary

`useLocalStorage<T>` gives you a clean, type‑safe API for persisting state to `localStorage`, automatically synchronizing across tabs and handling errors gracefully. It’s perfect for simple user preferences, UI state, or caching small amounts of data. For larger or more complex persistence needs, consider dedicated solutions (IndexedDB, server‑side storage, etc.).

123 t/s, 1706 tokens, 14s, 11%
