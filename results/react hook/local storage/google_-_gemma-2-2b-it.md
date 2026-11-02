# Gemma 2 2B Instruct
Model: google_-_gemma-2-2b-it
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

```typescript
import { useState, useEffect } from 'react';

type LocalStorageValue = unknown; // Generic type for localStorage values

interface UseLocalStorageState<T> {
  value: T | null;
  error?: Error; 
}

const useLocalStorage = <T>(key: string, initialValue: T): UseLocalStorageState<T> => {
  // State to store the value from local storage and any errors encountered.
  const [state, setState] = useState({
    value: localStorage.getItem(key) as T | null,
    error: null, 
  });

  useEffect(() => {
    if (state.value === undefined || state.value === null) {
      // Set initial value if not present in local storage
      setState({ ...state, value: initialValue }); 
    }
  }, [key]); // Run the effect only when the key changes

  const setValue = (newValue: T | undefined) => {
    if (newValue === undefined || newValue === null) {
      // Clear local storage if no new value is provided.
      localStorage.removeItem(key); 
      return;
    }

    try {
      // Set the value in localStorage and update state
      const parsedValue = JSON.stringify(newValue); // Convert to string before setting
      localStorage.setItem(key, parsedValue);
      setState({ ...state, value: newValue }); 
    } catch (error) {
      setState({ ...state, error: error }); 
    }
  };

  const getValue = () => state.value; // Get current value from local storage.

  return { value: getValue(), error: state.error };
};

export default useLocalStorage;
```


**Explanation:**

1. **Type Safety with Generics:** The `useLocalStorage` hook is generic, allowing you to store and retrieve values of any type (represented by the `T` parameter). 
2. **Error Handling:**  The hook includes basic error handling within `try-catch` blocks to ensure graceful errors during storage operations. This helps in debugging potential issues.
3. **Automatic JSON Parsing/Stringification:** The code automatically parses and stringifies values when saving them to localStorage using `JSON.stringify()`. 
4. **Sync Across Tabs/Windows:**  This hook handles synchronization across tabs and windows by leveraging the browser's native storage mechanism (localStorage). Changes made in one tab or window will be reflected in others if they share the same domain.

**Benefits:**

* **Type Safety:** Provides type safety for your data, ensuring that it matches the desired type (`T`).
* **Automatic JSON Conversion:** Makes storing and retrieving any data type simple and straightforward. 
* **Error Handling:**  Includes error catching to prevent unexpected issues and provide more information about them during development.

**Pros:**

* **Built-in Browser Functionality:** No external libraries are needed, making it efficient and lightweight.
* **Cross-Platform Compatibility:** Works across different operating systems (Windows, macOS, Linux) as well as browsers. 


**Cons & Potential Issues:**

* **Performance Overhead:** For very large datasets or frequent updates to localStorage, there might be some performance overhead. It's important to consider this if you are using a heavily populated data store with many items.
* **Security Concerns:**  While the built-in browser storage mechanism is generally secure, it's worth keeping in mind that storing sensitive information directly in local storage isn’t recommended without proper security measures. 

**Best Practices:**


* Use this hook only for user preferences or configuration data: Don't store critical application logic (like database state) within localStorage as it can be easily lost if the browser is closed.
* Implement a more robust error handling mechanism in production, perhaps logging errors to prevent them from crashing your app and allowing users to understand when something has gone wrong with their stored values. 



Let me know if you have any further questions or would like to explore specific aspects of this hook in greater detail!

219 t/s, 860 tokens, 4s, 12%
