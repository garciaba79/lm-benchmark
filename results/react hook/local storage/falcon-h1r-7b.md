# Falcon H1R 7B
Model: falcon-h1r-7b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

## `useLocalStorage<T>` – a self‑contained React hook  

Below is a TypeScript implementation that works out of the box with **React 18+**.  
It:

* reads/writes a value from `localStorage`,
* automatically JSON‑stringifies and parses,
* keeps component state in sync across all tabs/windows belonging to the same origin,
* cleans up listeners when the component unmounts,
* handles serialization errors gracefully and falls back to the supplied default.

```tsx
import { useState, useEffect, ReactEventTarget } from "react";

/**
 * Helper: read a value from localStorage.
 * Returns undefined if there is no entry or parsing fails.
 */
function getFromLocalStorage<T>(key: string): T | undefined {
    const raw = localStorage.getItem(key);
    if (!raw) return undefined;

    try {
        const parsed: any = JSON.parse(raw);
        // The generic type expects a proper T value. If parsing fails at runtime,
        // we simply hand back the default later.
        return parsed as T;
    } catch (e) {
        console.warn(`[useLocalStorage] Could not parse value for key="${key}":`, e);
        return undefined;
    }
}

/**
 * Helper: write a value to localStorage. Silently ignore non‑serializable values.
 */
function setToLocalStorage<T>(key: string, value: T): void {
    try {
        const json = JSON.stringify(value);
        // If the value is non‑serialisable JSON throws → caught above.
        if (json) localStorage.setItem(key, json);
    } catch (e) {
        console.error(`[useLocalStorage] Could not serialize value for key="${key}":`, e);
        // We simply do nothing; the caller will still have a valid component state.
    }
}

/**
 * React hook that mirrors data between a component and localStorage.
 * It automatically syncs across tabs/windows of the same origin.
 *
 * @param key          The storage key to use. Must be stable for the lifetime of the component.
 * @param initialValue Default value when no entry exists in localStorage or JSON parsing fails.
 */
export function useLocalStorage<T>(key: string, initialValue: T): [value: T, setValue: (v: T) => void] {
    // React state holds the component’s current value.
    const [value, setState] = useState(() => getFromLocalStorage<T>(key) as T);

    /**
     * Effect that:
     *   1️⃣ Installs a listener for `storage` events so other tabs can push updates.
     *   2️⃣ Persists the current value when the component mounts.
     *   3️⃣ Cleans up on unmount or key change.
     */
    useEffect(() => {
        // Storage event fires for any change to localStorage in the same origin,
        // including changes made by other tabs/windows.
        const handler: ReactEventTarget<string> = (event) => {
            // Only react when the key actually changed.
            if (event.key !== key) return;

            const newValue = getFromLocalStorage<T>(key);
            if (newValue !== value) setState(newValue as T);
        };

        window.addEventListener("storage", handler);

        // Persist the current component value right after we have read it.
        // This guarantees that a fresh page load will also see the same data later.
        try {
            setToLocalStorage<T>(key, value as any);
        } catch (_) {}

        // Cleanup listener when unmount or key changes.
        return () => window.removeEventListener("storage", handler);
    }, [key]); // re‑run on mount and if the key ever changes while mounted (unlikely).

    /** Setter that updates React state **and** localStorage atomically. */
    const setValue: (newVal: T) => void = useCallback(() => {
        setState(newVal);

        // Write after the render so we don’t fire a storage event for our own change.
        try {
            setToLocalStorage<T>(key, newVal);
        } catch (_) {}
    }, [key]);

    return [value as T, setValue];
}
```

### How to use it

```tsx
import React from "react";
import { useLocalStorage } from "./useLocalStorage";

export const Counter: React.FC = () => {
    const [count, setCount] = useLocalStorage("myCounter", 0);

    return (
        <div>
            <h2>Current count in localStorage: {count}</h2>
            <button onClick={() => setCount(c => c + 1)}>Increment</button>
            <button onClick={() => setCount(c => c - 1)}>Decrement</button>
        </div>
    );
};

export const App: React.FC = () => {
    return <Counter />;
};
```

Open two tabs to the same page and click buttons in one tab – both tabs will show the updated count instantly because of the `storage` event listener inside the hook.

---

## Benefits  

| What you gain | Why it matters |
|---|---|
| **Zero‑configuration persistence** | No server round‑trip, no Redux store, just a single state variable that survives page reloads and browser restarts. |
| **Cross‑tab synchronization** | The native `storage` event fires in every other tab/window of the same origin instantly when any code writes to localStorage. Perfect for things like UI preferences, theme toggles, or live collaborative state. |
| **Type safety (runtime)** | By declaring a generic `<T>` and using JSON serialization you get compile‑time type information on how the hook is used; at runtime the value will be parsed back into that exact shape as long as it’s serializable. |
| **No external dependencies** | Pure React + native browser APIs, works in any modern environment without pulling in a heavyweight store or custom polyfills. |
| **Graceful error handling** | The hook swallows serialization errors and falls back to the provided default value; you can extend it with callbacks if you need richer feedback. |

---

## Cons  

| Drawback | Detail / Mitigation |
|---|---|
| **Serialization limitation** | Only data that can be represented by JSON string → functions, circular references, `Date`, custom objects without a proper toJSON method will throw on `stringify`. The hook already catches the error but you lose those values silently. If you need such types consider providing a custom serializer/deserializer or store IDs instead of full objects. |
| **Size quota** | Most browsers expose ~5 MiB per origin for `localStorage`. Large arrays, deep nested structures, or many keys can exceed this limit and cause silent failures to write. Use a size‑aware wrapper or fallback storage (e.g., IndexedDB) if you anticipate large payloads. |
| **No built‑in expiration** | Values persist forever unless removed manually. If you need time‑limited data, add your own cleanup logic (`setTimeout(()=>localStorage.removeItem(...), TTL)` or store timestamps alongside the value). |
| **Race conditions on concurrent writes** | Two tabs may update at almost the same millisecond; whichever writes last wins. There is no conflict resolution built in. Resolve by implementing a version counter or debounce/`requestAnimationFrame`. |
| **Security** | LocalStorage is publicly readable via JavaScript, so never store secrets (tokens, passwords). Use cookies with HttpOnly/Secure flags for that purpose instead. |

---

## Potential Issues you might hit and how to address them  

1. **Non‑serializable values**  
   *Symptoms:* Component renders but sometimes shows the default value after a setState call; console logs show “Failed to serialize”.  
   *Fix:* Either restrict the type to plain objects/arrays, or add a custom serializer:

   ```ts
   const DATE_TAG = "__DATE__";
   export function useLocalStorage<T>(key: string, initialValue: T, options?: {
       serialize?: (value)=>string;
       deserialize?: (str)=>T;
   }) { /* implementation similar but uses options.serialize/deserialize */}
   ```

   Then call `useLocalStorage<MyState>(..., { serialize: dateToString, deserialize: stringToDate })`.

2. **Exceeding storage quota**  
   *Symptoms:* Write silently fails; later reads return undefined or default value.  
   *Fix:* Before persisting, check length:

   ```ts
   if (localStorage.length >= limit) console.warn("LocalStorage is full");
   // Optionally fallback to IndexedDB using idb library – but that would be an external dep.
   ```

3. **Component unmount leaving stale keys**  
   *Symptoms:* You forget you added a key for a temporary UI and it stays forever, consuming quota or leaking data between unrelated parts of the app.  
   *Fix:* Provide an extra cleanup utility:

   ```tsx
   const removeKeyFromLocalStorage = useCallback(() => localStorage.removeItem(key), [key]);
   return [value, setValue, React.useRef(removeKeyFromLocalStorage)];
   ```

   Call it when the component unmounts or when you want to clear a setting.

4. **Unexpected storage events from other origins**  
   *Symptoms:* When browsing on different sub‑domains (`app.example.com` vs `api.example.com`), updates in one domain leak into another, causing unwanted side effects.  
   *Fix:* The hook deliberately listens to the global `storage` event; you can narrow it by filtering events:

   ```ts
   if (event.origin !== window.location.origin) return;
   ```

5. **Performance spikes on many rapid changes**  
   *Symptoms:* Updating a setting hundreds of times per second may cause thousands of writes to localStorage, which is relatively slow compared with memory updates.  
   *Fix:* Debounce the internal setter:

   ```tsx
   const setValue = useCallback((val) => debounce(() => {/* actual logic */}, 10), [key]);
   ```

---

## TL;DR  

`useLocalStorage<T>` gives you a tiny, dependency‑free way to keep component state in the browser’s persistent storage while automatically synchronizing across all tabs of that origin. It works for any plain‐object data structure, survives reloads, and cleans up its event listeners on unmount. Keep an eye on serialization limits, size quotas, and security considerations, but for configuration‑type data (theme settings, UI layout preferences, shared counters) it’s often the simplest and most performant solution.

96 t/s, 6858 tokens, 72s, 43%
