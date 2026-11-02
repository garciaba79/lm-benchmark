# Deepseek Coder 6.7B Instruct
Model: deepseek-coder-6.7b-instruct
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is a simple implementation of useLocalStorage hook in TypeScript using React's built-in `useState` and `useEffect` hooks. This custom hook will read from local storage on mount, write to it when state changes, and remove the item from local storage when unmounting the component:

```tsx
import { useState, useEffect } from 'react';

function getStorageValue(key: string, initialValue: any) {
  const saved = localStorage.getItem(key);
  
  if (saved !== null) return JSON.parse(saved);
  
  if (initialValue instanceof Function) return initialValue();
  
  return initialValue;
}

export function useLocalStorage<T>(key: string, initialValue: T): [T, React.Dispatch<React.SetStateAction<T>>] {
  const [state, setState] = useState(() => getStorageValue(key, initialValue));
  
  // Write to local storage when state changes
  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(state))
    } catch (error) {
      console.warn('Error writing to localstorage: ', error);
    }
  }, [state]); // Only re-run if state changes
  
  // Cleanup on unmount
  useEffect(() => {
    return () => {
      try {
        localStorage.removeItem(key)
      } catch (error) {
        console.warn('Error removing from localstorage: ', error);
      }
    };
  }, []); // Empty array ensures this effect only runs once on unmount
  
  return [state, setState];
}
```
Benefits of using `useLocalStorage` hook:
- It provides a way to persist data across sessions and tabs. This is useful for user preferences or other settings that need to be remembered between page reloads/closes.
  
Pros: 
- Easy to use, just pass in the key and initial value like any other state variable.
- Automatically handles JSON parsing/stringifying so you don't have to do it manually.
- Handles errors gracefully by logging them instead of crashing your app.
  
Cons: 
- It relies on localStorage, which may not be available in certain environments (like server side rendering).
- If the state is complex or large, serializing/deserializing can take a significant amount of time and cause performance issues.
  
Potential Issues: 
- Local storage has limitations for storing data (usually around ~5MB), so if you're trying to store larger amounts of data, this could be an issue.
- If the state changes too frequently or in rapid succession, writing to localStorage can cause performance issues because it runs synchronously and blocks the main thread. This is mitigated by debouncing/throttling but may not always be desirable depending on use case. 
  
Overall, `useLocalStorage` hook provides a simple way to persist data across sessions using local storage in React applications without needing any external libraries or state management solutions like Redux or MobX. However, it's important to consider the potential issues and limitations of this approach when deciding whether to use it.

143 t/s, 741 tokens, 5s, 6%
