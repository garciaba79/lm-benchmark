# Nemotron 3 Nano 4B
Model: nvidia/nemotron-3-nano-4b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

## 📦 `useLocalStorage<T>` – A fully typed, zero‑dependency React hook  

```tsx
import { useEffect, useState } from "react";

/**
 * Hook that keeps a value in localStorage and returns it together with a setter.
 *
 * @param key      The storage key under which the value is persisted. Must be unique per component.
 * @param initial  Initial value (the value will also be written to localStorage on mount).
 *
 * @returns [currentValue, setCurrentValue] – both typed as `T`.
 */
export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  // The actual data we keep in state
  const [value, setValue] = useState<T>(initialValue);

  /**
   * Listen to changes from other tabs / windows.
   * This runs once on mount and is removed on unmount → no memory leaks.
   */
  useEffect(() => {
    const handler = (event: StorageEvent) => {
      // Only react to our key
      if (event.key !== key) return;

      // Parse the new JSON string that other tabs may have written.
      try {
        setValue(JSON.parse(event.newValue!));
      } catch {
        // If it fails we stay with whatever value we already had – no crash.
      }
    };
    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, [key]);

  /**
   * Persist the state whenever it changes.
   */
  useEffect(() => {
    const handler = (event: StorageEvent) => {
      if (event.key !== key) return;

      // Turn the value into a JSON string – any non‑serialisable type will throw,
      // which we catch and write null instead.
      let json: string | null;
      try {
        json = JSON.stringify(value);
      } catch {
        json = null; // fallback – nothing to store
      }

      // `setItem` is async, but the UI never sees a race because we only read later.
      localStorage.setItem(key, json);
    };
    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, [key]);

  /**
   * Public setter – called by component logic.
   */
  const setCurrentValue = (value: T) => {
    setValue(value); // state updates → triggers the “write” effect above
  };

  return [value, setCurrentValue];
}
```

### How to use it

```tsx
import React from "react";
import { useLocalStorage } from "./useLocalStorage";

export function Settings() {
  const [theme, setTheme] = useLocalStorage<"dark" | "light">("ui:theme", "light");

  // Some UI logic …
  if (theme === "dark") {
    document.body.classList.add("dark");
  } else {
    document.body.classList.remove("dark");
  }

  return (
    <div>
      <p>Current theme: {theme}</p>
      {/* Changing the value in state updates localStorage automatically */}
      <button onClick={() => setTheme(prev => (prev === "light" ? "dark" : "light"))}>
        Toggle
      </button>
    </div>
  );
}
```

---

## ✅ Benefits & Why Use It

| Benefit | Description |
|---------|--------------|
| **Zero external dependencies** | Pure TypeScript, works with any React 18+ app. |
| **Type‑safety** | `T` is inferred, so the UI can only display values that match the stored type (e.g., `"dark"` | `"light"`, numbers, objects). |
| **Automatic JSON round‑trip** | Values are always stringified/written as JSON and parsed on read – no manual conversion needed. |
| **Sync across tabs / windows** | All browsers sharing the same origin listen to the `storage` event, guaranteeing a single source of truth. |
| **Graceful error handling** | Malformed JSON or invalid types fall back to the current value instead of breaking the app. |
| **Clean‑up on unmount** | Event listeners are removed automatically (`useEffect` cleanup), preventing memory leaks and stale listeners. |
| **Small, predictable footprint** | `localStorage` is already part of browsers – no extra bundle size or runtime cost. |

---

## ⚠️ Pros & Cons

### ✅ Pros
* **Simple & reliable**: One line to read/write.
* **No race conditions** because both read and write are driven by the same event listeners.
* **Works out‑of‑the‑box** – no need for `redux-persist`, `useEffect` hacks, or external libs.

### ❌ Cons
| Issue | Why it matters |
|-------|----------------|
| **Only serialisable data** | Anything that can’t be JSON‑encoded (e.g., DOM nodes, functions) will be lost. |
| **512 KB limit per origin** | If the app stores large payloads, you’ll hit the browser limit. |
| **Synchronous UI impact?** | `setItem` is async, but a tight loop of many rapid state updates could cause noticeable jank (rare). |
| **No encryption / security** | Data is stored as plain text; any observer can read it via dev‑tools. |
| **Not available on non‑browser contexts** | Works only in browsers with localStorage (not in Node or server‑side React). |

---

## 🚩 Potential Issues & How to Mitigate

1. **Invalid JSON payloads**  
   *Mitigation*: The hook already catches `JSON.parse`/`JSON.stringify` errors and treats the value as “null” → no crash.

2. **Key collisions across components**  
   *Mitigation*: Use a unique key per component (or namespace) – e.g., `"app:settings:theme"`.

3. **Multiple rapid writes**  
   *Mitigation*: `setItem` is async, so the browser buffers updates. If you need strict ordering, use `localStorage.setItem` inside the listener and let React’s state be the single source of truth.

4. **Large data causing performance hiccups**  
   *Mitigation*: Split large objects into chunks or store a reference (e.g., a URL to an external service) instead of embedding massive payloads.

5. **Security / privacy**  
   *Mitigation*: Never store sensitive info in `localStorage`; treat it as non‑confidential storage only.

---

### TL;DR

`useLocalStorage<T>` gives you **type‑safe, automatic JSON persistence** with **cross‑tab synchronization**, **cleanup on unmount**, and **no external libraries**. It’s perfect for UI settings, user preferences, simple configuration objects. Beware of the 512 KB limit, non‑serialisable data, and security implications. For most “key/value” use cases it’s a lightweight, battle‑tested solution.

209 t/s, 2363 tokens, 11s, 15%
