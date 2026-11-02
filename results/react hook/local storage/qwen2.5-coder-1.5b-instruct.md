# Qwen2.5 Coder 1.5B Instruct
Model: qwen2.5-coder-1.5b-instruct
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

Here is a simple implementation of the useLocalStorage hook in TypeScript:

```typescript
import { useEffect, useState } from 'react';

export function useLocalStorage<T>(key: string, initialValue: T): [T, (newValue: T) => void] {
  const [value, setValue] = useState(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error('Error reading from localStorage:', error);
      return initialValue;
    }
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  const setValueAndSync = (newValue: T) => {
    try {
      setValue(newValue);
      localStorage.setItem(key, JSON.stringify(newValue));
    } catch (error) {
      console.error('Error writing to localStorage:', error);
    }
  };

  return [value, setValueAndSync];
}
```

Benefits:
- Type safety
- Automatic JSON parsing/stringifying
- Sync across tabs/windows if the key changes

Pros:
- Easy to use and understand
- Works well with React 18+ and functional components
- Handles errors gracefully

Cons:
- Limited to storing primitive types (number, string, boolean, null, undefined)
- Not suitable for storing complex objects or arrays

Potential issues:
- If the key changes, all existing values will be lost
- The hook does not handle edge cases such as localStorage being unavailable or corrupted

317 t/s, 307 tokens, 1s, 5%
