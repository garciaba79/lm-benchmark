# Gemma 4 E4B
Model: google/gemma-4-e4b
Test: Hook Local Storage
Created: 11/03/2026, 12:37:30 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is a complete implementation of the `useLocalStorage` hook in TypeScript, along with detailed explanations.

## The `useLocalStorage` Hook

```tsx
import { useState, useEffect, useCallback } from 'react';

/**
 * A custom React hook that synchronizes state with localStorage and keeps it type-safe.
 * It automatically handles JSON serialization/deserialization and attempts to sync across tabs.
 *
 * @template T The expected type of the stored value.
 * @param {string} key The key under which the value is stored in localStorage.
 * @param {T} initialValue The default value if nothing is found in localStorage.
 * @returns {[T, React.Dispatch<React.SetStateAction<T>>]} A tuple containing the current state and a setter function.
 */
export function useLocalStorage<T>(key: string, initialValue: T): [T, React.Dispatch<React.SetStateAction<T>>] {
  // 1. Initialize State from localStorage or use provided default
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      if (item) {
        return JSON.parse(item) as T;
      }
      // If nothing is stored, use the initial value provided to useState
      return initialValue;
    } catch (error) {
      // Handle cases where localStorage might be unavailable or corrupted
      console.error(`Error reading local storage for key "${key}":`, error);
      return initialValue;
    }
  });

  // 2. Effect to synchronize state changes back to localStorage
  useEffect(() => {
    try {
      const serializedState = JSON.stringify(storedValue);
      localStorage.setItem(key, serializedState);
    } catch (error) {
      console.error(`Error writing to local storage for key "${key}":`, error);
    }
  }, [key, storedValue]); // Dependencies: Re-run if the value changes or the key changes

  // 3. Handle Cross-Tab Synchronization (The Listener Effect)
  // This effect listens for storage events fired by other tabs/windows accessing localStorage with the same key.
  useEffect(() => {
    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === key && event.newValue !== null) {
        try {
          // Only update state if the change came from an external source (a different tab)
          const newValue: T = JSON.parse(event.newValue);
          console.log(`[useLocalStorage] Synced value received from another tab for key "${key}".`);
          setStoredValue(newValue);
        } catch (e) {
          console.error("Failed to parse synchronized local storage data:", e);
        }
      }
    };

    // Attach the listener
    window.addEventListener('storage', handleStorageChange);

    // Cleanup function: Important for preventing memory leaks
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key]); // Re-run this effect only if the key itself changes

  // Return the value and the setter function
  return [storedValue, setStoredValue];
}
```

---

## Usage Example (How to use it in a component)

To demonstrate type safety and usage:

```tsx
import React from 'react';
import { useLocalStorage } from './useLocalStorage'; // Assuming you saved the hook above

// Define an interface for better structure and type checking
interface UserSettings {
  theme: 'dark' | 'light';
  notificationsEnabled: boolean;
}

const SettingsComponent: React.FC = () => {
  // 1. Initialize state using a complex object (requires initial value)
  const [settings, setSettings] = useLocalStorage<UserSettings>(
    'user-prefs', 
    { theme: 'light', notificationsEnabled: true }
  );

  // Handler that updates the local state
  const handleThemeChange = (newTheme: 'dark' | 'light') => {
    setSettings(prev => ({ ...prev, theme: newTheme }));
  };

  return (
    <div>
      <h1>User Settings</h1>
      <p>Current Theme: <strong>{settings.theme}</strong></p>
      <button onClick={() => handleThemeChange('dark')}>Set Dark Mode</button>
      <button onClick={() => handleThemeChange('light')} style={{ marginLeft: '10px' }}>Set Light Mode</button>

      <hr />
      <label>
        Enable Notifications:
        <input
          type="checkbox"
          checked={settings.notificationsEnabled}
          onChange={(e) => setSettings(prev => ({ ...prev, notificationsEnabled: e.target.checked }))}
        />
      </label>

      <p style={{ marginTop: '20px', borderTop: '1px solid #ccc', paddingTop: '10px' }}>
        <em>Check the browser console or open another tab with this component to see sync in action!</em>
      </p>
    </div>
  );
};

export default SettingsComponent;
```

---

## Explanation and Analysis

### 🚀 Benefits & Pros

1. **Type Safety (TypeScript Generics `<T>`):** This is the biggest win. By using generics, TypeScript knows that `storedValue` will always be of type `T`, and when you call `setStoredValue`, it enforces the structure defined by `T`.
2. **Automatic Serialization/Deserialization:** It completely abstracts away the manual process of `JSON.stringify()` before writing and `JSON.parse()` upon reading, preventing common runtime errors.
3. **Cross-Tab Synchronization:** By listening to the global `storage` event, it automatically updates the component's state whenever another tab or window modifies the same local storage key, providing a near-real-time feel across sessions/tabs.
4. **Error Handling (Robustness):** It wraps all `localStorage` interactions (`getItem`, `setItem`) in `try...catch` blocks and handles potential failures gracefully by logging errors and falling back to the initial state or default values, preventing application crashes if storage is disabled or corrupted.
5. **Cleanup:** The use of `useEffect`'s return function ensures that the event listener is properly removed when the component unmounts, thus preventing memory leaks.

### ⚠️ Cons & Potential Issues

1. **Synchronous Nature of `localStorage`:** Reading/Writing to `localStorage` is synchronous and happens on the main thread. If you store extremely large amounts of data or perform many read/write operations rapidly, it can potentially block the UI briefly (though this is rare for typical state management).
2. **Storage Quotas:** The browser imposes limits on how much data can be stored per origin (usually 5-10MB). Exceeding this limit will cause `setItem` to fail, which our error handling mitigates by logging the failure.
3. **Read-Write Race Conditions (Caveat):** While the cross-tab listener handles *external* updates, if two tabs update the state simultaneously and rapidly, a race condition *could* theoretically occur where one tab overwrites the other's intended change before the `storage` event propagates correctly. However, for most standard use cases, this pattern is robust enough.

### 🛠️ Performance Consideration

The dependency array in the primary `useEffect`: `[key, storedValue]` is crucial. It ensures:
1. **Initial Load:** The state is loaded only once on mount (via the initial `useState` callback).
2. **Writes:** The effect runs *every time* `storedValue` changes, ensuring immediate persistence to storage.

### Conclusion

The `useLocalStorage` hook provided above is a professional-grade utility that solves common boilerplate headaches associated with client-side persistent state management in React. It balances **convenience**, **type safety**, and **robustness** while correctly handling browser APIs like the global `storage` event for multi-tab synchronization.

143 t/s, 1753 tokens, 12s
