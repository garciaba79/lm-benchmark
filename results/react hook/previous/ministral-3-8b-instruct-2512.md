# Ministral 3 8B Instruct 2512
Model: ministral-3-8b-instruct-2512
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a `usePrevious` hook written in TypeScript that works with React 18+ hooks (using the new concurrent features if needed) and handles all types correctly:

```typescript
import { useEffect, useRef } from 'react';

function usePrevious<T>(value: T): T | undefined {
  const previousValueRef = useRef<T>();

  useEffect(() => {
    // Store current value in ref before it updates
    previousValueRef.current = value;
  }, [value]); // Only re-run if value changes

  return previousValueRef.current;
}

export default usePrevious;
```

### Key Features:

1. **Generic Type Support**: Works with any type `T` (string, number, object, etc.)
2. **Initial Render Handling**: Returns `undefined` on first render (since there's no previous value)
3. **Performance Optimized**:
   - Only updates when the input `value` changes
   - Uses `useRef` for stable reference between renders
4. **Concurrent React Compatible**: Works with React 18+ features

### Usage Example:

```typescript
import usePrevious from './usePrevious';

function Counter() {
  const [count, setCount] = useState(0);
  const previousCount = usePrevious(count);

  return (
    <div>
      Current: {count}
      Previous: {previousCount || 'None'}
    </div>
  );
}
```

### Alternative Version (if you want to track all values):

If you need to track the value even when it's the same reference (like with objects), you could use this version:

```typescript
function usePrevious<T>(value: T): T | undefined {
  const previousValueRef = useRef<T>();

  useEffect(() => {
    // Create a new ref for each render to detect changes
    const currentValueRef = { current: value };
    previousValueRef.current = currentValueRef;
  }, [value]);

  return previousValueRef.current?.current;
}
```

This second version will track changes even when the same object reference is passed (like with `{x: 1}` vs `{x: 2}`). Choose whichever fits your use case better.

125 t/s, 457 tokens, 4s, 6%
