# DeepSeek v4 Pro Qwen3.5 9B UNCENSORED Heretic
Model: deepseek-v4-pro-qwen3.5-9b-uncensored-heretic
Test: Hook Previous
Created: 11/18/2026, 11:46:26 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a clean implementation of `usePrevious` in TypeScript using only React 18+ hooks:

```tsx
import { useEffect, useRef } from 'react';

/**
 * Returns the previous value of a given dependency.
 * 
 * @param value - The current value to track changes for
 * @returns The previous value, or undefined on initial render
 */
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    // Store the previous value before updating it with the current one
    ref.current = value;
  }, [value]);

  return ref.current;
}

export default usePrevious;
```

## How it works:

1. **`useRef<T | undefined>(undefined)`** - Creates a mutable reference that persists across renders without triggering re-renders.

2. **`useEffect(() => { ... }, [value])`** - Runs after every render when `value` changes (or on the initial mount). Inside, we update `ref.current` to the current value.

3. **Return** - Returns `ref.current`, which holds:
   - `undefined` on the very first render (before any effect runs)
   - The previous value after the first render
   - Updates correctly when the input changes

## Usage example:

```tsx
function Counter() {
 const [count, setCount] = useState(0);
 
 const prevCount = usePrevious(count);
 
 return (
 <div>
 <p>Current count: {count}</p>
 <p>Previous count: {prevCount ?? 'N/A'}</p>
 <button onClick={() => setCount(prev => prev + 1)}>
 Increment
 </button>
 </div>
 );
}
```

## Key points:

- ✅ **Generic type T** - Works with any value (number, string, object, etc.)
- ✅ **Initial render handling** - Returns `undefined` on first render before the effect runs
- ✅ **No external libraries** - Only uses React's built-in hooks
- ✅ **React 18+ compatible** - Uses modern patterns

The hook is efficient because it only re-runs when the dependency changes, and the ref doesn't cause unnecessary re-renders.

132 t/s, 499 tokens, 4s
