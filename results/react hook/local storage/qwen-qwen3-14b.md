# Qwen3 14B
Model: qwen/qwen3-14b
Test: Hook Local Storage
Created: 11/03/2026, 01:10:54 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here's a fully typed React custom hook called `useLocalStorage<T>` that reads from and writes to `localStorage` with support for JSON parsing/stringifying, type safety, cross-tab synchronization (via `BroadcastChannel`), error handling, and cleanup on unmount using **React 18+** features.

---

## ✅ `useLocalStorage<T>(key: string, initialValue: T)` Hook

### 💡 Features:
- Type-safe with generics `<T>`
- JSON parsing/stringifying
- Cross-tab synchronization (when the key changes)
- Graceful error handling
- Cleanup on unmount
- Uses React 18+ features like `useEffect` without `useLayoutEffect`
- No external libraries required

---

### 📦 Code:

```tsx
import { useEffect, useState } from 'react';

type UseLocalStorageOptions<T> = {
  parse?: (value: string) => T;
  stringify?: (value: T) => string;
};

// Custom hook for localStorage with cross-tab sync and type safety
export function useLocalStorage<T>(
  key: string,
  initialValue: T,
  options: UseLocalStorageOptions<T> = {}
): [T, React.Dispatch<React.SetStateAction<T>>] {
  const { parse = JSON.parse as (value: string) => T, stringify = JSON.stringify } = options;

  // State to hold the value
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? parse(item) : initialValue;
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Sync across tabs using BroadcastChannel
  useEffect(() => {
    if (!('BroadcastChannel' in window)) {
      console.warn("BroadcastChannel is not supported in this browser.");
      return;
    }

    const channel = new BroadcastChannel(key);

    const handleMessage = (event: MessageEvent) => {
      try {
        setStoredValue(parse(event.data));
      } catch (error) {
        console.error(`Error syncing localStorage key "${key}":`, error);
      }
    };

    channel.addEventListener('message', handleMessage);

    return () => {
      channel.removeEventListener('message', handleMessage);
      channel.close();
    };
  }, [key, parse]);

  // Update localStorage whenever the state changes
  useEffect(() => {
    try {
      window.localStorage.setItem(key, stringify(storedValue));
    } catch (error) {
      console.warn(`Error writing to localStorage key "${key}":`, error);
    }
  }, [key, storedValue, stringify]);

  return [storedValue, setStoredValue];
}
```

---

## 🧪 Example Usage:

```tsx
import React from 'react';
import { useLocalStorage } from './useLocalStorage';

function App() {
  const [user, setUser] = useLocalStorage('user', { name: 'Guest' });

  return (
    <div>
      <h1>User Name: {user.name}</h1>
      <input
        type="text"
        value={user.name}
        onChange={(e) => setUser({ ...user, name: e.target.value })}
      />
    </div>
  );
}

export default App;
```

---

## 🔍 Benefits

- **Type Safety**: Uses TypeScript generics `<T>` to ensure correct types.
- **Auto Parse/Serialize**: Automatically handles JSON parsing and stringifying.
- **Cross-tab Sync**: Uses `BroadcastChannel` to sync state across tabs/windows when the value changes.
- **Graceful Error Handling**: Catches errors during localStorage access without crashing the app.
- **No External Dependencies**: Built-in browser APIs only (JSON, BroadcastChannel).

---

## 🛡️ Pros

| Pros |
|------|
| No external libraries needed |
| Full type safety with generics |
| Cross-tab synchronization |
| Simple and reusable API |
| Works in React 18+ with hooks |

---

## ⚠️ Cons & Potential Issues

| Cons / Potential Issues |
|-------------------------|
| **Browser Compatibility**: `BroadcastChannel` is not supported in older browsers (e.g., IE, Safari < 16). You may need a polyfill or fallback.
| **Storage Limits**: localStorage has size limits (~5MB), so large objects can cause errors.
| **Security Risks**: Storing sensitive data in localStorage may expose it to XSS attacks. Use caution with private info.
| **Performance Overhead**: Syncing across tabs using `BroadcastChannel` could have minor performance implications in heavy apps.

---

## ✅ Best Practices

- Avoid storing sensitive information like passwords or access tokens in localStorage.
- For large datasets, consider using IndexedDB instead.
- Handle parsing errors gracefully (e.g., fallback to defaults).
- Use the optional `parse` and `stringify` props if you need custom serialization logic (e.g., date objects).

---

Let me know if you'd like a version that supports **IndexedDB** or uses **Redux Toolkit** for syncing.

79 t/s, 1050 tokens, 13s
