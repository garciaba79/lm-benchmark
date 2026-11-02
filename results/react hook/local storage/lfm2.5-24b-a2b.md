# LFM2.5 24B A2B
Model: lfm2.5-24b-a2b
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

## 1️⃣  The hook – `useLocalStorage<T>`

```tsx
import { useState, useEffect } from 'react';

/**
 * A generic React hook that syncs a value with the browser’s localStorage.
 *
 * @param key          – The storage key to read/write (must be unique per tab)
 * @param initialValue – The value used when there is no stored entry
 * @returns            [currentValue, setter] – works like useState / onChange
 */
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, React.Dispatch<React.SetStateAction<T>>] {
  /* --------------------------------------------------------------
   * 1️⃣  Initialise state lazily – try to read from localStorage.
   *    If the stored JSON is corrupted we fall back to `initialValue`.
   * -------------------------------------------------------------- */
  const [value, setValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue; // SSR guard
    try {
      const raw = localStorage.getItem(key);
      if (raw !== null) {
        return JSON.parse(raw) as T;
      }
    } catch (e) {
      console.warn('useLocalStorage – failed to parse stored value for', key, e);
    }
    // No valid data → use the supplied initial value
    return initialValue;
  });

  /* --------------------------------------------------------------
   * 2️⃣  Keep other tabs/windows in sync via the `storage` event.
   * -------------------------------------------------------------- */
  useEffect(() => {
    const handleStorage: StorageEvent = (e) => {
      if (e.key !== key || e.newValue === null) return;
      try {
        const parsed = JSON.parse(e.newValue) as T;
        setValue(parsed);
      } catch (err) {
        console.warn('useLocalStorage – could not parse storage change', err);
        // optional: fall back to the original default
        setValue(initialValue);
      }
    };

    window.addEventListener('storage', handleStorage as EventListener);
    return () => {
      window.removeEventListener('storage', handleStorage as EventListener);
    };
  }, [key, initialValue]);

  /* --------------------------------------------------------------
   * 3️⃣  Persist every change to localStorage.
   * -------------------------------------------------------------- */
  useEffect(() => {
    try {
      const serialized = JSON.stringify(value);
      if (typeof window !== 'undefined') {
        localStorage.setItem(key, serialized);
      }
    } catch (err) {
      console.error('useLocalStorage – failed to write', key, err);
    }
  }, [value]);

  return [value, setValue];
}
```

### How it works

| Step | What happens |
|------|--------------|
| **Lazy init** | On the first render we read `localStorage[key]`. If parsing fails or the key is missing we fall back to the `initialValue` passed to the hook. |
| **Cross‑tab sync** | A global `storage` listener fires whenever *any* tab writes/removes a value with the same `key`. The handler parses the new JSON and updates React’s state, so all open windows stay up‑to‑date. |
| **Write‑back** | Whenever `value` changes (including programmatic updates via `setValue`) we `JSON.stringify` it and store it back to localStorage – this also triggers the cross‑tab listener for other tabs. |
| **Cleanup** | The effect that installs the listener removes it on unmount, preventing memory leaks. |

---

## 2️⃣  Example usage (TSX)

```tsx
import React from 'react';
import { useLocalStorage } from './useLocalStorage';

type UserPrefs = {
  language: string;
  darkMode: boolean;
};

const PreferencesPage: React.FC = () => {
  // The hook will read “user-prefs” or fall back to a default object
  const [prefs, setPrefs] = useLocalStorage<UserPrefs>('user-prefs', {
    language: 'en',
    darkMode: false,
  });

  const toggleDark = () => setPrefs(p => ({ ...p, darkMode: !p.darkMode }));

  return (
    <div>
      <h2>Preferences</h2>
      <label>
        Language:
        <select value={prefs.language} onChange={e =>
          setPrefs(p => ({ ...p, language: e.target.value as UserPrefs['language'] }))
        }>
          <option value="en">English</option>
          <option value="de">German</option>
          <option value="fr">French</option>
        </select>
      </label>

      <label>
        Dark mode:
        <input
          type="checkbox"
          checked={prefs.darkMode}
          onChange={() => toggleDark()}
        />
      </label>

      {/* Show current state for demo */}
      <pre>{JSON.stringify(prefs, null, 2)}</pre>
    </div>
  );
};

export default PreferencesPage;
```

*When the component unmounts, the `storage` listener is removed automatically.*

---

## 3️⃣  Benefits & Pros

| ✅ Advantage | Why it matters |
|--------------|----------------|
| **Zero‑dependency persistence** – no extra npm packages. | Keeps bundles small, especially for simple apps. |
| **Type‑safe API** – generic `<T>` guarantees compile‑time checking of the stored payload. | Catches mismatches early (e.g., trying to assign a `string` where an object is expected). |
| **Automatic JSON handling** – no manual `JSON.stringify/parse`. | Reduces boilerplate and eliminates a common source of bugs. |
| **Cross‑tab sync** via the native `storage` event. | Users get consistent state even if they open multiple windows or switch between tabs/windows (e.g., a settings page in a different tab). |
| **Simple functional hook** – integrates with any React state pattern (`useState`, `useReducer`). | Easy to drop into existing components without refactoring. |

---

## 4️⃣  Cons & Potential Issues

| ⚠️ Drawback / Caveat | Details |
|----------------------|---------|
| **Only works with JSON‑serializable values** – objects that contain functions, Dates (converted to strings) or circular references will break the storage layer. | Keep data simple; if you need richer types, serialize them yourself before calling the hook. |
| **Race conditions on rapid changes** – a fast series of `setValue` calls can fire multiple writes to localStorage. The last one wins (as with any persisted state). | Acceptable for most UI‑state use‑cases; not suited for high‑frequency real‑time data. |
| **SSR incompatibility** – `localStorage` is undefined in the server environment. The hook guards against that, but you must still avoid calling it at the top level of a server component. | If you render on the server (Next.js), keep the call inside a client‑only wrapper or use a conditional check. |
| **Memory / performance** – large objects get stringified on every change; for huge payloads this could be noticeable. | For typical settings / UI state it’s negligible, but worth noting in data‑heavy apps. |
| **No built‑in undo/redo** – the history of changes is not exposed. | If you need a history, you’d have to build another layer on top of `useLocalStorage`. |

---

## 5️⃣  TL;DR Checklist for Using This Hook

- ✅ Provide a **unique key** (e.g., `"user‑prefs"`).  
- ✅ Ensure the **initial value** is valid JSON or something you can safely parse.  
- ✅ Use it inside a **functional component** (or any custom hook).  
- ✅ Remember that cross‑tab sync only works when the *same* origin & key are used.  
- ✅ The hook already handles cleanup of the `storage` event listener – nothing extra is required.

---

### Bottom line

`useLocalStorage<T>` gives you a **type‑safe, zero‑dependency** way to keep data in `localStorage` while automatically keeping multiple browser tabs in sync and handling parse errors gracefully. It’s perfect for persisting UI preferences, form state, or any small “sticky” data that should survive page reloads without pulling in a full state‑management library.

103 t/s, 4477 tokens, 44s, 28%
