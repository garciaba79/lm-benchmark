# Lfm2 24B A2B
Model: liquid/lfm2-24b-a2b
Test: Hook Window Size
Created: 11/03/2026, 01:22:11 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is a complete implementation of the `useWindowSize` hook in TypeScript, following best practices for React 18+ and proper cleanup.

### The Hook Implementation

```typescript
import { useState, useEffect } from 'react';

/**
 * Custom hook to track the current window dimensions.
 * Automatically updates on window resize and cleans up event listeners.
 */
export function useWindowSize(): { width: number; height: number } {
  // State to store the current dimensions
  const [dimensions, setDimensions] = useState<{ width: number; height: number }>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  // Effect to handle initial setup and cleanup
  useEffect(() => {
    // Function to update state when the window resizes
    const handleResize = () => {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Add the resize event listener
    window.addEventListener('resize', handleResize);

    // Cleanup function to remove the event listener when the component unmounts or before re-running
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty dependency array ensures this runs only once on mount/demount

  return dimensions;
}
```

### How It Works

1.  **State Initialization**: The hook starts by setting the initial state using `window.innerWidth` and `window.innerHeight`. This ensures the value is correct immediately when the component renders.
2.  **Event Listener**: Inside `useEffect`, we define a `handleResize` function that updates the state with the latest window dimensions whenever the user resizes the browser.
3.  **Subscription**: We attach this function to the `resize` event using `window.addEventListener`.
4.  **Cleanup**: The return value of `useEffect` is a cleanup function. This function runs before the component unmounts or if the effect re-runs (which it won't here due to the empty array), ensuring we remove the listener to prevent memory leaks.

### Usage Example

```tsx
import React from 'react';
import { useWindowSize } from './useWindowSize';

const WindowDimensionsDisplay: React.FC = () => {
  const { width, height } = useWindowSize();

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, zIndex: 1000 }}>
      Window Size: {width}px x {height}px
    </div>
  );
};

export default WindowDimensionsDisplay;
```

This component will display the current window size and update it automatically as the browser is resized.

146 t/s, 610 tokens, 4s
