# LFM2.5 24B A2B
Model: lfm2.5-24b-a2b
Test: Hook Window Size
Created: 11/03/2026, 01:37:02 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a clean TypeScript implementation using only React 18+ hooks. The hook returns an object `{ width, height }` that updates on window resize and cleans up the event listener when the component unmounts.

```tsx
import { useEffect, useState } from 'react';

export interface WindowSize {
  width: number;
  height: number;
}

/**
 * Hook that provides the current window dimensions.
 * Updates automatically when the browser window is resized.
 */
export function useWindowSize(): WindowSize {
  const [size, setSize] = useState<WindowSize>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    // Stable handler created once on mount
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Attach listener on mount, remove it on unmount (cleanup)
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty deps → runs only once

  return size;
}
```

**How it works:**

1. **Initial state** – On mount, `useState` initializes the size from the current `window.innerWidth/Height`.
2. **Event listener** – The `useEffect` hook adds a `'resize'` listener when the component mounts.
3. **Update on resize** – Each resize triggers `handleResize`, which calls `setSize` with fresh dimensions, causing a re-render with updated values.
4. **Cleanup** – On unmount (or before the effect runs again), the cleanup function removes the event listener to prevent memory leaks.

No external libraries are used; only React's built‑in hooks (`useState`, `useEffect`) are employed.

138 t/s, 1534 tokens, 11s
