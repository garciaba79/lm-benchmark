# Qwen3.5 9B The Defiant Fable Uncnr Heretic NEO MAX
Model: qwen3.5-9b-the-defiant-fable-uncensored-heretic-neo-imatrix-max-mtp
Test: Hook Previous
Created: 11/22/2026, 02:55:30 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```ts
import { useEffect, useRef } from 'react';

/**
 * usePrevious - Returns the previous value of a given state/prop.
 *
 * @param value - The current value to track.
 * @returns The previous value on subsequent renders; undefined on the first render.
 */
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    // Store the current value for next render
    ref.current = value;
  }, [value]);

  return ref.current;
}
```

105 t/s, 131 tokens, 1s, 1%
