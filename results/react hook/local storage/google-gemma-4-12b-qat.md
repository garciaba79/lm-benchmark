# Gemma 4 12B QAT
Model: google/gemma-4-12b-qat
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is a robust, production-ready implementation of a `useLocalStorage` hook in TypeScript.

### The Implementation

```tsx
import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * A hook to synchronize state with localStorage.
 * @param key - The localStorage key.
 * @param initialValue - The initial value if no value is found in localStorage.
 * @returns The state and a setter function.
 */
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  // Use a ref to keep track of the initial value to avoid unnecessary re-renders
  const isInitialMount = useRef(true);

  // 1. Initialize state
  // We use a function inside useState so it only runs once during the initial render
  const [state, setState] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // 2. Define the setter function
  const setLocalStorage = useCallback((value: T | ((val: T) => T)) => {
    try {
      // Handle functional updates (e.g., setState(prev => ...))
      const valueToStore = value instanceof Function ? value(state) : value;

      window.localStorage.setItem(key, JSON.stringify(valueToStore));
      
      // Update state to trigger re-render in the current component
      setState(valueToStore);
    } catch (error) {
      console.error(`Error writing to localStorage key "${key}":`, error);
    }
  }, [key]);

  // 3. Handle Cross-Tab Synchronization
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      // Only update if the key changed in another tab
      if (e.key === key && e.newValue !== null) {
        try {
          const value = JSON.parse(e.newValue as string) as T;
          setState(value);
        } catch (error) {
          console.error(`Error parsing storage event for "${key}":`, error);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [key]);

  // 4. Handle Local Tab Updates (Optional but recommended)
  // This ensures that if you have multiple components using the same key 
  // in the same tab, they all update simultaneously.
  useEffect(() => {
    const handleStorageEvent = (e: StorageEvent) => {
        // Standard 'storage' event doesn't fire in the same window.
        // For same-tab sync, we rely on the shared setState via the setter.
    };
    // Note: For same-tab synchronization across multiple components, 
    // a Context Provider is usually required.
  }, [key]);

  return [state, setLocalStorage];
}

export default useLocalStorage;
```

---

### How to use it

```tsx
function App() {
  const [theme, setTheme] = useLocalStorage<string>('app-theme', 'light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <div className={theme}>
      <p>Current theme: {theme}</p>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </div>
  );
}
```

---

### Detailed Explanation

#### Benefits
1.  **Type Safety**: By using a generic `<T>`, TypeScript ensures that the value you pull out of `localStorage` matches the type you defined, preventing "string-only" errors common with native `localStorage`.
2.  **Cross-Tab Sync**: It listens to the `storage` event. If a user has your app open in two tabs and changes a setting (like "Dark Mode") in one, the other tab updates automatically.
3.  **Functional Updates**: The setter supports functional updates (e.g., `setCount(prev => prev + 1)`), which is essential for maintaining state integrity during rapid updates.
4.  **Error Resilience**: It wraps `JSON.parse` and `localStorage.setItem` in try/catch blocks. This prevents the app from crashing if `localStorage` is full or contains corrupted data.

#### Pros
*   **Persistence**: State survives page refreshes.
*   **No Dependencies**: Zero bundle size impact as it uses native Web APIs.
*   **Automatic Serialization**: Automatically handles objects and arrays by converting them to strings.

#### Cons
*   **Synchronous API**: `localStorage` is synchronous. If you are reading/writing massive amounts of data (multi-megabyte JSONs), it can block the main thread and cause UI jank.
*   **Storage Limits**: Browsers limit `localStorage` to ~5MB. It is not suitable for large datasets.
*   **SSR Issues**: Because `window` is not available during Server Side Rendering (Next.js/Remix), this hook must be used inside `useEffect` or guarded with a check (though the current implementation is safe because `useState` initializer only runs on the client in most standard setups, but a check `typeof window !== 'undefined'` is safer for strict SSR).

#### Potential Issues & Best Practices
1.  **The "Same-Tab" Limitation**: The native `storage` event **only fires in other tabs**. If you have two components in the *same* tab using `useLocalStorage('my-key')`, changing one will not automatically update the other.
    *   *Fix*: To solve this, you should wrap this hook in a **Context Provider**. This way, all components share the same state instance.
2.  **Data Corruption**: If a user manually edits `localStorage` with invalid JSON, the `JSON.parse` will fail. The hook handles this by logging an error and falling back to `initialValue`.
3.  **Privacy**: Never store sensitive information (PII, passwords, session tokens) in `localStorage` as it is vulnerable to XSS attacks. For tokens, use `HttpOnly` cookies.

86 t/s, 1421 tokens, 17s, 9%
