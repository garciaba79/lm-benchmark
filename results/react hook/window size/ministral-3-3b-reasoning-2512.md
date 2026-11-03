# Ministral 3 3B Reasoning 2512
Model: ministral-3-3b-reasoning-2512
Test: Hook Window Size
Created: 11/02/2026, 11:49:22 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is the implementation of the `useWindowSize` hook in TypeScript using React 18+ hooks:

```typescript
import { useState, useEffect } from 'react';

const useWindowSize = () => {
  const [dimensions, setDimensions] = useState<{ width: number; height: number }>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty dependency array to run only once on mount

  return dimensions;
};

export default useWindowSize;
```

This hook:
1. Uses `useState` to store the current window dimensions, initialized with `window.innerWidth` and `window.innerHeight`.
2. Sets up a resize event listener in `useEffect` that updates the state whenever the window is resized.
3. Includes cleanup to remove the event listener when the effect unmounts or dependencies change (though since the dependency array is empty, it will only run on unmount).
4. Returns the dimensions object `{ width: number, height: number }`.

The hook is designed to work in React 18+ and does not rely on external libraries, as required. It updates automatically when the window is resized and handles cleanup properly by removing the event listener when no longer needed.

190 t/s, 2731 tokens, 14s
