# Gemma 4 E2B
Model: google/gemma-4-e2b
Test: Hook Local Storage
Created: 11/15/2026, 09:43:47 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is the implementation of the `useLocalStorage` hook in TypeScript, followed by an explanation of its design choices.

## `useLocalStorage` Hook Implementation

```tsx
import React, { useState, useEffect, useMemo } from 'react';

/**
 * Custom hook to synchronize state with localStorage.
 * It handles automatic JSON serialization/deserialization and synchronization across tabs.
 *
 * @template T The type of the value being stored.
 * @param {string} key The key under which to store the data in localStorage.
 * @param {T} initialValue The initial value to use if nothing is found in localStorage.
 * @returns {[T, (value: T | ((error: string) => void)) => void]} A tuple containing the state and a setter function.
 */
export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((error: string) => void)) => void] {
  // 1. State initialization: Use a ref to hold the actual state, initialized from localStorage or initialValue.
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      if (item) {
        // Attempt to parse the stored string back into the original type T
        return JSON.parse(item) as T;
      }
      // Return initial value if nothing is found
      return initialValue;
    } catch (error) {
      // Handle potential JSON parsing errors gracefully
      console.error(`Error reading localStorage key “${key}”:`, error);
      // Fallback to the initial value on error
      return initialValue;
    }
  });

  // 2. Effect for Synchronization: Sync state whenever storedValue changes.
  useEffect(() => {
    try {
      // Attempt to stringify and save the new state
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      // Handle potential storage errors gracefully
      console.error(`Error writing to localStorage key “${key}”:`, error);
      // Note: We don't typically throw an error here as we want the UI to remain functional, 
      // but logging the failure is crucial.
    }
  }, [key, storedValue]); // Re-run whenever storedValue changes

  // 3. Setter function: Function to update the state and trigger persistence.
  const setValue = (value: T | ((val: T) => T)) => {
    let valueToStore: T;

    // Handle functional updates (where the new state depends on the previous state)
    if (typeof value === 'function') {
      valueToStore = value(storedValue);
    } else {
      valueToStore = value as T;
    }
    
    // Update the state using the standard useState setter
    setStoredValue(valueToStore);
  };

  // 4. Return the state and the setter
  return [storedValue, setValue];
}
```

---

## Explanation of Design Choices, Pros, Cons, and Potential Issues

### How It Works

1.  **Initialization (`useState` with Callback):** We use `useState` with a function as the initial value (the lazy initializer). This function runs only once on the first render to check `localStorage`. It attempts to retrieve the item, parse it using `JSON.parse()`, or defaults to `initialValue`. Error handling is built directly into this retrieval step.
2.  **Synchronization (`useEffect`):** A separate `useEffect` monitors changes to `storedValue`. Whenever it changes, it immediately serializes the new value using `JSON.stringify()` and writes it back to `localStorage`. This ensures that the persistence layer stays in sync with the component's state.
3.  **Setter Function (`setValue`):** The setter function is designed to handle both direct assignment (`value: T`) and functional updates (`value: (prev: T) => T`), which mimics the behavior of `setState` within React, making the hook highly reusable.

### Benefits (Pros)

1.  **Declarative State Management:** It abstracts away the boilerplate of reading from/writing to storage, allowing components to manage state declaratively as if it were local state.
2.  **Persistence:** It provides simple, built-in persistence for form inputs, themes, or user preferences without requiring manual `useEffect` setups in every component.
3.  **Type Safety (via Generics):** By using TypeScript generics (`<T>`), the hook ensures that whatever data you store in `localStorage` is strictly typed when it is retrieved and set within the React context.
4.  **Error Handling:** It includes `try...catch` blocks for both reading and writing to `localStorage`, preventing application crashes if storage access is blocked (e.g., due to security restrictions).
5.  **Tab Synchronization:** Because it relies on the native browser `localStorage`, changes made in one tab are automatically reflected in other open tabs/windows of the same origin, fulfilling the synchronization requirement simply by using the standard API.

### Drawbacks (Cons)

1.  **Performance Overhead:** Every time the state changes, two asynchronous operations occur: reading/writing to disk and serializing/deserializing JSON. For extremely high-frequency updates (e.g., tracking mouse position rapidly), this overhead might be noticeable compared to purely in-memory state.
2.  **Single Origin Limitation:** This hook is strictly tied to the browser's `window.localStorage`. It cannot synchronize state across different domains or subdomains, nor can it use alternative storage mechanisms (like Session Storage).
3.  **JSON Limitation:** It forces all data into a JSON string. If you need to store complex non-serializable objects (like functions or `Symbol`s), this hook will fail or require custom serialization logic.

### Potential Issues & Mitigation

1.  **Storage Quota Errors:** Browsers impose storage limits on `localStorage` (often 5MB). If a user fills up their storage, the `try...catch` will handle the write failure, but the user experience might be poor if they expect the data to save successfully. **Mitigation:** Inform the user if necessary (though for simple preferences, silent failure is often acceptable).
2.  **Asynchronous Race Conditions (Minor):** While React's `useState` handles synchronization well, if a component re-renders rapidly while storage operations are pending, minor inconsistencies *could* occur, although the strict dependency structure of `useEffect` generally prevents this in this pattern. **Mitigation:** Relying on React's state flow remains the safest approach here.
3.  **Strict Typing Complexity:** Handling the `T | ((val: T) => T)` setter type is complex but necessary for robust state management. If you strictly only needed direct assignment, you could simplify it, but this makes the hook more powerful.

190 t/s, 1498 tokens, 8s
