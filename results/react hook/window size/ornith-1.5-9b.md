# Ornith 1.5 9B
Model: ornith-1.5-9b
Test: Hook Window Size
Created: 11/02/2026, 01:00:39 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a clean, well-typed `useWindowSize` hook:

```typescript
import { useState, useEffect } from 'react';

export interface WindowSize {
  width: number;
  height: number;
}

/**
 * Tracks the current window dimensions and updates them on resize.
 * Safe to use in both client and server environments.
 */
export function useWindowSize(): WindowSize {
  const [size, setSize] = useState<WindowSize>({ width: 0, height: 0 });

  useEffect(() => {
    // Guard against SSR where `window` is not defined
    if (typeof window === 'undefined') return;

    const updateSize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Read dimensions immediately so the first render reflects real values
    updateSize();

    window.addEventListener('resize', updateSize);

    // Cleanup on unmount (or before re-running) to avoid memory leaks / duplicate listeners
    return () => {
      window.removeEventListener('resize', updateSize);
    };
  }, []);

  return size;
}
```

### How it works

- **`useState`** holds the `{ width, height }` object.
- **`useEffect`** subscribes to the `resize` event and returns a cleanup function that removes the listener — this is what makes it safe for unmounting and re-running effects.
- The initial `updateSize()` call ensures the first render already has real dimensions instead of waiting for the (often delayed) resize event to fire.
- The `typeof window === 'undefined'` guard prevents crashes during server-side rendering / static generation.

### Usage

```tsx
import { useWindowSize } from './useWindowSize';

export default function Layout() {
  const { width, height } = useWindowSize();

  return (
    <div style={{ padding: `${height}px`, fontSize: `${width / 100}px` }}>
      {width} × {height}
    </div>
  );
}
```

### Notes & possible enhancements

- **Throttling:** For very high-frequency resize handling (e.g., heavy layout recalculation), you can wrap `updateSize` in a `requestAnimationFrame` or debounce. The default fires on every resize event, which is fine for most cases.
- **More accurate sizing:** If you need dimensions that account for scrollbars/content changes rather than just the viewport, swap the listener for a `ResizeObserver` on `document.documentElement`. Let me know if you'd like that variant.

Want me to add an optional callback (e.g., `(size) => void`) or support breakpoint-based values?

137 t/s, 1137 tokens, 8s
