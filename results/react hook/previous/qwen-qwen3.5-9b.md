# Qwen3.5 9B
Model: qwen/qwen3.5-9b
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

# usePrevious Hook in TypeScript

Here's a complete `usePrevious` hook implementation for React 18+ with proper TypeScript typing, support for any generic type T, and correct handling of initial renders:

```typescript
import { useRef, useEffect } from 'react';

/**
 * A custom React hook that returns the previous value of a given dependency.
 * 
 * @param value - The current value whose previous state you want to access
 * @returns The previous value from the last render (undefined on first render)
 * 
 * @example
 * const [count, setCount] = useState(0);
 * const prevCount = usePrevious(count);
 * useEffect(() => {
 *   console.log('Count changed from', prevCount, 'to', count);
 * }, [count]);
 */
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Optional utility exports for common types and usage
export type PreviousValue<T> = T | undefined;

export function usePreviousString(value: string): string | undefined {
  return usePrevious(value);
}

export function usePreviousNumber(value: number): number | undefined {
  return usePrevious(value);
}
```

## Example Usage

```tsx
import React, { useState, useEffect } from 'react';
import { usePrevious } from './usePrevious';

function CounterExample() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  useEffect(() => {
    if (prevCount !== undefined) {
      console.log(`Count changed from ${prevCount} to ${count}`);
    }
  }, [count]);

  return (
    <div>
      <h1>{count}</h1>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

## Behavior Summary

- ✅ **First Render:** Returns `undefined`, indicating no previous value exists.
- ✅ **Subsequent Renders:** Returns the value from the last render before this one.
- ✅ **Generic Support:** Works with any type (strings, numbers, objects, etc.).
- ✅ **React 18+ Compatible:** Uses only built-in hooks (`useRef`, `useEffect`).

This hook is reliable for tracking state changes and comparing values across renders without external dependencies.

119 t/s, 2054 tokens, 17s, 13%
