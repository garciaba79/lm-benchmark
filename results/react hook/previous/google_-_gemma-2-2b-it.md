# Gemma 2 2B Instruct
Model: google_-_gemma-2-2b-it
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```typescript
import { useState } from 'react';

type Previous<T> = T; // Define a generic for previous values

const usePrevious = <T>(value: unknown): [T | null, () => void] => {
  const [previousValue, setPreviousValue] = useState(null);

  React.useEffect(() => {
    if (previousValue === null && value !== null) {
      setPreviousValue(value); 
    }
  }, [value]);

  return [previousValue, () => {
    // Reset the previous state when called
    setPreviousValue(null);
  }];
};

export default usePrevious; 
```


**Explanation:**

1. **`usePrevious<T>`**: This is a custom hook that takes an arbitrary type `T`. The `<T>` signifies it's generic, allowing us to work with any data type in the React component. 
2. **`type Previous<T> = T;`**: This defines the type of the previous value as just itself (`T`). 
3. **`useState(null)`:** We use `useState(null)` to store the previous value, initially setting it to null.

4. **`React.useEffect(() => { ... }, [value])`**: The useEffect hook triggers after every render and gets called when the provided dependencies change (in this case just the 'value'). 
    - If we encounter a new value,  we set the `previousValue`.


**Usage:**

```typescript
import usePrevious from './usePrevious'; // Assuming your hook is in a file named 'usePrevious.ts'

function MyComponent() {
  const [count, setCount] = useState(0); 
  const [prevCount, setPrevCount] = usePrevious(count);

  // Example usage:
  const handleClick = () => {
    setCount((prev) => prev + 1);
  };

  return (
    <div>
      <p>Current count: {count}</p>
      {/* Use previous value after the first render */}
      {prevCount && <p>Previous count: {prevCount}</p>}
      <button onClick={handleClick}>Increment</button>
    </div>
  ); 
}

```



**Key Points:**


* **React Hooks Only:** This hook uses only React hooks, ensuring compatibility with modern React versions. It avoids external libraries for a more lean and self-contained solution.
* **Type Safety:** The `usePrevious` hook is type-safe thanks to the generic parameter `<T>`. 



Let me know if you have any other questions!

212 t/s, 571 tokens, 3s, 8%
