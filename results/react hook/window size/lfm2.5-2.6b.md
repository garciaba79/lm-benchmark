# LFM2.5 2.6B
Model: lfm2.5-2.6b
Test: Hook Window Size
Created: 11/02/2026, 11:33:54 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is the React hook implementation using only built-in React 18+ hooks.

```typescript
import { useState, useEffect } from 'react';

// Define the shape of the returned object for TypeScript safety
interface WindowDimensions {
  width: number;
  height: number;
}

/**
 * A custom hook to track the current window size.
 *
 * It subscribes to the browser's resize event and updates the state immediately,
 * ensuring the values are always in sync with the current viewport dimensions.
 */
export const useWindowSize = (): WindowDimensions => {
  // State to hold the current width and height
  const [windowSize, setWindowSize] = useState<WindowDimensions>({
    width: 0,
    height: 0,
  });

  useEffect(() => {
    // The effect runs once on mount. We add a listener for window resize events.
    const handleResize = () => {
      // Update state with the current dimensions
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);

    /**
     * Cleanup function to remove the event listener when the component unmounts.
     * This prevents memory leaks and ensures we don't update state after the component is gone.
     */
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty dependency array ensures this runs only on mount (React 18+)

  return windowSize;
};
```

### How it works:

1.  **State**: We use `useState` to store the `width` and `height`. The initial value defaults to `{ width: 0, height: 0 }`.
2.  **Effect**: We use `useEffect` with an empty dependency array (`[]`). This ensures the resize listener is set up exactly once when the component mounts.
3.  **Listener**: Inside the effect, we define a handler function that reads `window.innerWidth` and `window.innerHeight` and calls `setWindowSize`.
4.  **Cleanup**: The `return () => { ... }` block inside `useEffect` is crucial. It runs when the component unmounts to call `window.removeEventListener`, preventing memory leaks.

### Example Usage:

```tsx
import React from 'react';
import { useWindowSize } from './useWindowSize';

const App = () => {
  const { width, height } = useWindowSize();

  return (
    <div style={{ width: `${width}px`, height: `${height}px` }}>
      Current Window Size: {width}x{height}
    </div>
  );
};

export default App;
```

241 t/s, 1894 tokens, 8s
