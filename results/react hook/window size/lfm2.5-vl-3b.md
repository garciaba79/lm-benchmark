# LFM2.5 VL 3B
Model: lfm2.5-vl-3b
Test: Hook Window Size
Created: 11/02/2026, 11:35:02 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is the implementation of `useWindowSize`.

I have used the `useRef` hook to store the last known dimensions so we can compare them in the effect to trigger a re-render when the window actually changes size (rather than triggering on every render cycle).

```typescript
import { useEffect, useRef } from 'react';

export function useWindowSize(): { width: number; height: number } {
  // Use refs to store the last known dimensions so we don't poll the window on every render.
  const lastWidth = useRef<number>(0);
  const lastHeight = useRef<number>(0);

  useEffect(() => {
    const handleResize = () => {
      // Update state only if there is a change in values
      if (lastWidth.current !== window.innerWidth || lastHeight.current !== window.innerHeight) {
        lastWidth.current = window.innerWidth;
        lastHeight.current = window.innerHeight;
      }
    };

    window.addEventListener('resize', handleResize);

    // Cleanup: remove the event listener when the component unmounts
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return { width: lastWidth.current, height: lastHeight.current };
}
```

### Key Details:
1.  **`useRef`**: Used to store `width` and `height`. This allows us to compare the current value with the previous one without causing unnecessary re-renders.
2.  **Event Listener**: The `resize` event is added inside the effect. It runs only when the window actually changes size (e.g., user drags the browser).
3.  **Cleanup**: The `useEffect` cleanup function removes the listener to prevent memory leaks if the component is reused or unmounted prematurely.
4.  **Type Safety**: The return type explicitly defines `{ width: number; height: number }`.

234 t/s, 405 tokens, 2s
