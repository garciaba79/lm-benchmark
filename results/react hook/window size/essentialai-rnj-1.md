# Rnj 1
Model: essentialai/rnj-1
Test: Hook Window Size
Created: 11/02/2026, 12:48:41 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

It seems there is a mix-up in the request; the requirement is for a React hook written in TypeScript that returns current window dimensions, which doesn't align with the initial mention of Python. However, given the problem description and your expertise in Python, I'll provide the correct solution in TypeScript rather than Python.

Here's how to write the `useWindowSize` hook in TypeScript:

```typescript
import { useState, useEffect } from 'react';

function useWindowSize(): { width: number; height: number } {
  const [windowSize, setWindowSize] = useState<{ width: number; height: number }>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    // Add event listener for resize
    window.addEventListener('resize', handleResize);

    // Call handler right away so state gets updated with initial window size
    handleResize();

    // Remove event listener on cleanup
    return () => window.removeEventListener('resize', handleResize);
  }, []); // Empty array ensures that effect is only run on mount and unmount

  return windowSize;
}

export default useWindowSize;
```

This `useWindowSize` hook initializes the window size with the current dimensions. It listens for the `resize` event and updates the state accordingly. The cleanup function removes the event listener when the component unmounts, avoiding potential memory leaks.

125 t/s, 306 tokens, 2s
