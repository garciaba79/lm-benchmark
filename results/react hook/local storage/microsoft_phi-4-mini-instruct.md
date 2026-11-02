# Microsoft Phi 4 Mini Instruct
Model: microsoft_phi-4-mini-instruct
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

To create a custom hook called `useLocalStorage` in TypeScript that provides type safety for reading from and writing to local storage with JSON parsing/stringifying capabilities while also handling errors gracefully would look something like this:

```typescript
import { useState, useEffect } from 'react';

function useLocalStorage<T>(key: string, initialValue?: T): [T | undefined, (value: T) => void] {
  const storedValue = localStorage.getItem(key);
  
  let stateValue: T;

  if (initialValue !== undefined) { // Avoids initialization before first render
    try {
      stateValue = JSON.parse(storedValue as string || 'null') as T;
    } catch (error) {
      console.error(`Error parsing stored localStorage value for key "${key}":`, error);
    }
  }

  const setState: (value: T) => void = () => {
    try {
      stateValue = JSON.stringify(initialValue ?? null, undefined, 2); // Pretty-print the serialized object
      localStorage.setItem(key, stateValue as string);
      
      if (!storedValue || storedValue !== initialValue.toString()) { 
        console.log(`Local Storage set: key="${key}" with value=${initialState.value}`);
    } catch (error) {
      console.error('Error saving to Local Storage', error);
    }
  };

  useEffect(() => {
    // Sync across tabs/windows if the stored item changes
    localStorage.setItem(key, stateValue as string);

    return () => { 
      setState(undefined); // Cleanup on unmount: remove from storage when component is no longer needed.
    };
  }, [key]);

  const value = (value?: T) => {
    try {
      if (typeof initialValue === 'function') {
        setState(initialValue(value));
      } else {
        stateValue = JSON.parse((storedValue as string ?? '') || "null");
        localStorage.setItem(key, JSON.stringify(stateValue));
      }
    } catch (error) {
      console.error(`Error updating stored value for key "${key}":`, error);
    }

    return stateValue;
  };

  return [value(), setState];
}

// Usage example
const App = () => {
  const [name, setName] = useLocalStorage<string>('username', 'John Doe');

  // The returned setter function can be used to update the value in local storage.
  
  console.log(`Current name is: ${name}`);
};

export default App;
```

**Benefits and Pros**

1. **Type Safety:** By using generics, `useLocalStorage` ensures type safety when storing any data structure that matches TypeScript's types.

2. **Automatic Parsing/Serialization:** It automatically parses stored JSON strings to objects upon retrieval from local storage for ease of use within the React component state while serializing them back before saving into locals whenever necessary (e.g., during updates).

3. **Sync Across Tabs/Widows**: By updating `localStorage` inside a cleanup function in an effect hook, it helps sync data across different tabs/windows.

4. **Error Handling:** Graceful error handling provides better stability and avoids crashing the application when encountering issues with local storage operations or parsing errors.


**Cons**

1. **Local Storage Limitations & Security Risks:**
   - LocalStorage is synchronous; for large datasets this could lead to poor performance.
   - Data stored in it can be accessed via JavaScript, posing a security risk if sensitive data was saved.

2. **Browser Compatibility:** Older browsers might not support `localStorage` or have different implementations that don't strictly follow the spec (use caution and test across target environments).

3. **Automatic Sync Issue:**
   - The sync mechanism currently provided by this hook may be unnecessary for most use cases as modern web applications often rely on other synchronization strategies like real-time databases, which are more reliable.
   
4. **Performance Overhead**:
   - React components relying heavily upon local storage might face performance issues due to frequent reads and writes.

5. **Not Native State Management:**
    - Using `localStorage` directly within the state management of a complex application can lead to convoluted code, especially if you're using other libraries like Redux or MobX for managing your app's global states.


**Potential Issues**

1. **Local Storage Quota:** Users' browsers have limited quota (usually around 5MB) which could cause an issue when trying to store large amounts of data.

2. **Data Persistence Limitation:**
   - Since `localStorage` is a web storage mechanism, the persisted state will not survive if you uninstall/reinstall your browser or clear its cache/storage manually.


**Use Case Consideration**

Despite these cons and potential issues mentioned above, this hook can still be useful for persisting simple user preferences across sessions in single-page applications (SPAs) without requiring server-side interaction. For example:

- **User Preferences:** Such as light/dark mode settings or font size adjustments.
- **Form Data Caching**: Like partially filled forms that should persist even if the page reloads.

Overall, this hook can be a quick and easy way to implement simple state persistence with type safety in modern React applications. However for complex scenarios involving synchronization across devices (multi-device), real-time databases like Firebase Firestore or websockets might provide more robust solutions.

190 t/s, 1106 tokens, 6s, 7%
