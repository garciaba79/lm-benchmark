# Qwen3.5 9B
Model: qwen/qwen3.5-9b
Test: Hook Window Size
Created: 11/02/2026, 01:08:39 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```tsx
import { useEffect, useState } from 'react';

interface WindowSize {
  width: number;
  height: number;
}

/**
 * A custom React hook to track window size in real-time.
 * Updates on resize events and cleans up properly on unmount.
 */
export function useWindowSize(): WindowSize {
  const [dimensions, setDimensions] = useState<WindowSize>({ width: 0, height: 0 });

  useEffect(() => {
    // Handle initial mount
    const handleResize = (): void => {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Initial measurement
    handleResize();

    // Add resize event listener
    const unsubscribe = window.addEventListener('resize', handleResize);

    // Cleanup on unmount or before component re-renders
    return () => {
      window.removeEventListener('resize', unsubscribe as EventListener);
    };
  }, []);

  return dimensions;
}
```

121 t/s, 376 tokens, 3s
