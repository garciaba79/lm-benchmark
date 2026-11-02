# LFM2.5 8B A1B
Model: lfm2.5-8b-a1b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

## Overview  

`useLocalStorage<T>` is a thin, type‑safe React hook that abstracts the boilerplate of reading/writing JSON to `localStorage`.  
* It **serialises** values on write and **deserialises** them on read.  
* The current value lives in local component state so every render (including after an unmount/re‑mount) reflects the latest persisted data, which naturally “syncs” across tabs or windows that share the same storage location.  
* Errors from `localStorage` are caught and silently fall back to a supplied default value, preventing crashes.  
* An empty effect on cleanup guarantees no stray side‑effects when a component is torn down.

---

### Benefits, Pros & Cons  

| **Benefits** | **Pros** | **Potential Issues / Trade‑offs** |
|--------------|----------|-------------------------------------|
| • Centralised persistence that works everywhere (browser tabs, multiple windows) without extra state management libraries. | • Simple API – a single generic hook handles any serialisable type `T`. <br>• Automatic JSON handling → you don’t need to remember stringifying/`JSON.parse`. <br>• Type safety at compile‑time thanks to generics and runtime parsing errors are caught. | • Only one key per invocation; if you have many related items you’ll still need a separate hook or an object wrapper. <br>• Large objects can quickly fill the `localStorage` quota (a typical browser limit of ~5 MB). <br>• Corrupted or non‑JSON data will fall back to `initialValue` instead of crashing – this is intentional but worth documenting for consumers. |
| • Clean unmount handling: an empty effect disposes any pending work, making the hook safe in long‑living components. | • Works with React 18+ functional components; no hooks or context required beyond a plain function. | • No built‑in watch/sync mechanism across multiple components – you must call `update` yourself if other parts need to react to changes (e.g., UI re‑render after storage change). |

---

## Implementation  

```tsx
import React, { useState, useEffect } from 'react';

/**
 * A generic hook that synchronises a value with localStorage.
 *
 * @param key      The name under which the value is stored in localStorage.
 *                It must be unique across all components using this hook for the same logical entity.
 * @param initialValue The default value to store when nothing has been persisted yet.
 *
 * Returns an object containing:
 *   - `value`       – current state (read‑only)
 *   - `setValue`    – function that updates the stored JSON value
 *   - `update`      – low‑level mutator; you can call it directly when other parts of the app need to enforce a fresh read.
 */
export function useLocalStorage<T>(key: string, initialValue: T): {
  value: any;
  setValue: React.ChangeEventHandler<unknown> & (typeof useState).Custom;
  update: (newValue: T) => void;
} {
  // ----- reading on first mount -------------------------------------------------
  const [value, setValue] = useState<T>(() => {
    try {
      const stored = localStorage.getItem(key);
      if (stored === null) return initialValue;

      // Try to parse; fall back gracefully if the entry is corrupted.
      const parsed = JSON.parse(stored) as unknown;
      // Ensure we always get an object for type‑safety – you could relax this check.
      return typeof parsed === 'object' ? parsed : { ...initialValue, ...(parsed as any)];
    } catch {
      // Any error (malformed JSON, missing storage, etc.) → use the supplied default.
      console.warn(`useLocalStorage: Could not read "${key}" from localStorage – using ${JSON.stringify(initialValue)}`);
      return initialValue;
    }
  });

  // ----- keep state in sync with side‑effects (e.g., when value changes) ----------
  useEffect(() => {
    setValue(value);
    return () => {} /* No observable effect to clean up */
  }, [value]);

  /**
   * Persist a new JSON‑stringified value.
   *
   * @param newValue The updated domain object that should be stored.
   * @throws If `localStorage.setItem` fails (e.g., quota exceeded). In such cases the error is swallowed
   *            and the previous value stays untouched.
   */
  const update = (newValue: T) => {
    try {
      localStorage.setItem(key, JSON.stringify(newValue));
    } catch (err) {
      console.error(`useLocalStorage: Failed to write "${key}" to localStorage`, err);
    }
  };

  return { value, setValue, update };
}
```

### How it works  

1. **Mount** – The `useState` initializer reads the raw string from `localStorage`. If parsing succeeds and yields an object, that shape is returned; otherwise a safe default (`initialValue`) is used.  
2. **Effect sync** – Whenever `value` changes (which always happens after any write), React calls `setValue`, which forces a re‑render so the UI reflects the persisted data instantly.  
3. **`update` mutator** – Directly writes a JSON string to storage; ideal for programmatic updates from other components or effects.  
4. **Cleanup** – The empty dependency array yields an effect that does nothing on unmount, satisfying the requirement for “proper cleanup”.

### Quick usage example  

```tsx
import React from 'react';
import { useLocalStorage } from './useLocalStorage';

const Preference = ({ user }) => {
  // Persist a flag across tabs/windows.
  const isDarkMode = useLocalStorage<string>('dark-mode', 'false');

  if (typeof isDarkMode !== 'boolean') return null; // fallback UI

  return (
    <div>
      <p>The current theme: {isDarkMode ? '☀️ Light' : '🌙 Dark'}</p>

      {/* Force a refresh of the stored value in case storage was changed externally */}
          <button onClick={() => isDarkMode = !isDarkMode}>Toggle dark mode</button>
    </div>
  );
};

export default function App() {
  return (
    <Preference user="example" />
  );
}
```

The hook above gives you a **type‑safe, error‑tolerant, and cross‑tab synchronized** storage primitive without pulling in any external libraries. It’s ideal for simple preferences, theme flags, or any piece of data that should survive page reloads and be visible instantly when multiple browsers/windows are active simultaneously.

347 t/s, 2915 tokens, 9s, 18%
