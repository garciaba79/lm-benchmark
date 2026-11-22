# Qwen3.5 9B The Defiant Fable Uncnr Heretic NEO MAX
Model: qwen3.5-9b-the-defiant-fable-uncensored-heretic-neo-imatrix-max-mtp
Test: Hook Window Size
Created: 11/22/2026, 02:55:49 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```tsx
import { useEffect, useState } from 'react';

/**
 * Hook that tracks the current window size and updates it on resize.
 * Returns an object with width and height in pixels.
 */
export function useWindowSize(): { width: number; height: number } {
  const [size, setSize] = useState<{ width: number; height: number }>(() => ({
    width: window.innerWidth,
    height: window.innerHeight,
  }));

  useEffect(() => {
    // Handler for resize events
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Attach event listener
    window.addEventListener('resize', handleResize);

    // Cleanup on unmount or before re-render with new dependencies (if any)
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return size;
}
```

99 t/s, 214 tokens, 2s, 2%
