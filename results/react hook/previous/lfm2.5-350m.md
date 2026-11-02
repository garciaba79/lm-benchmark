# LFM2.5 350M
Model: lfm2.5-350m
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```typescript
import { useState } from 'react';

const usePrevious = <T>(value: T) => {
  const [prevValue, setPrevValue] = useState<T>();

  return { prevValue, setPrevValue };
};

export default usePrevious;
```

742 t/s, 66 tokens, 0s, 1%
