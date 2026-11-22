# Qwen3.6 35B A3B
Model: qwen/qwen3.6-35b-a3b
Test: Hook Previous
Created: 11/22/2026, 12:45:32 PM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```typescript
import { useRef, useEffect } from 'react';

export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  });

  return ref.current;
}
```

49 t/s, 63 tokens, 1s, 1%
