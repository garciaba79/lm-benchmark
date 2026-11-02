# Ministral 3 3B Instruct 2512
Model: ministral-3-3b-instruct-2512
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a `usePrevious` React hook for TypeScript that works with React Hooks rules (no external dependencies) and handles generic types correctly:

```typescript
import { useEffect, useRef } from 'react';

function usePrevious<T>(value: T): T | undefined {
    const ref = useRef<T | undefined>();

    useEffect(() => {
        ref.current = value;
    }, [value]);

    return ref.current;
}

export default usePrevious;
```

### How it works:
1. Uses `useRef` to store the previous value between renders
2. Updates the reference on every render (using dependency array `[value]`)
3. Returns either the stored previous value or `undefined` for initial renders

### Usage example:
```typescript
import React, { useState } from 'react';
import usePrevious from './usePrevious';

function Counter() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>Current count: {count}</p>
      {prevCount !== undefined && <p>Previous count was: {prevCount}</p>}
    </div>
  );
}
```

### Key features:
- Works with any type `T` (generic)
- Returns `undefined` on first render
- Only uses React Hooks rules (no external dependencies)
- Maintains proper TypeScript typing

This implementation follows React's hook rules by only calling hooks at the top level of components/functions.

216 t/s, 314 tokens, 2s, 6%
