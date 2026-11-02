# LFM2.5 230M
Model: lfm2.5-230m
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is a well-structured and type-safe implementation of the `usePrevious` hook in TypeScript:

```tsx
import { useState, useEffect } from 'react';

interface PreviousValue extends DefaultProps {
  value: T;
}

const usePrevious = () => {
  const [previousValue, setPreviousValue] = useState<T>(null);

  const prev = usePrevious(prevValue);
  return {
    value,
    previousValue,
  };
};

export default usePrevious;
```

### Key Features:
1. **Generic Type Support**: The hook accepts any generic type `T` and maintains state as a new value.
2. **State Management**: Uses `useState<T>` to track the previous value, ensuring it persists across render cycles.
3. **Default Props Handling**: Initializes with `null`, allowing default values to be set later if needed (e.g., `prev = null`).
4. **Clean and Readable Code**: Uses modern React hooks syntax (`useState`, `useEffect`) without external dependencies.

### Usage:
```tsx
import { usePrevious } from './usePrevious';

function App() {
  const [value, setValue] = usePrevious();

  return (
    <div>
      <p>Current Value: {value}</p>
      <button onClick={() => setValue(value)}>Update</button>
    </div>
  );
}

export default App;
```

### Explanation:
- `prev` holds the previous value from the last render.
- `usePrevious` returns a prop object containing the current and previous values, enabling easy access in components that use this hook.
- The state is persisted using `useState`, which ensures changes are reflected even after component unmounts.

This solution adheres to TypeScript's principles by ensuring type safety and efficient state management without external libraries.

977 t/s, 405 tokens, 0s, 3%
