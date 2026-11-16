# Gemma 4 E2B
Model: google/gemma-4-e2b
Test: Hook Window Size
Created: 11/15/2026, 09:44:09 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is the implementation of the `useWindowSize` custom React hook in TypeScript, which updates automatically on window resize and handles cleanup correctly.

### `useWindowSize.ts`

```typescript
import { useState, useEffect } from 'react';

/**
 * Interface for the window dimensions returned by the hook.
 */
export interface WindowSize {
  width: number;
  height: number;
}

/**
 * A custom React hook that tracks and provides the current dimensions of the browser window.
 * It updates whenever the window is resized.
 *
 * @returns {WindowSize} An object containing the current width and height of the window.
 */
export function useWindowSize(): WindowSize {
  // State to store the window dimensions
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    // Handler function to update the state when the window is resized
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Add the event listener for the resize event
    window.addEventListener('resize', handleResize);

    // Cleanup function: This is crucial. It removes the event listener 
    // when the component unmounts or the effect re-runs, preventing memory leaks.
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty dependency array ensures this effect runs only once on mount and cleanup on unmount

  // Return the current window size
  return windowSize;
}
```

### How to Use It (Example Component)

Here is an example demonstrating how you would use this hook in a functional React component:

```tsx
import React from 'react';
import { useWindowSize } from './useWindowSize'; // Adjust the path as necessary

const WindowDisplay: React.FC = () => {
  // Consume the hook
  const { width, height } = useWindowSize();

  return (
    <div>
      <h1>Window Size Tracker</h1>
      <p>Current Width: {width}px</p>
      <p>Current Height: {height}px</p>
      <p>Resize the browser window to see the values update automatically.</p>
    </div>
  );
};

export default WindowDisplay;
```

### Explanation of Key Concepts

1.  **`useState`**: Used to store the current `width` and `height`. It initializes them with the current window dimensions upon mounting.
2.  **`useEffect`**: This hook is responsible for setting up and tearing down the side effect (listening for resize events).
    *   **Setup**: Inside the `useEffect`, we attach an event listener to the global `window` object for the `'resize'` event. When the resize event fires, the `handleResize` function updates the state using `setWindowSize`.
    *   **Cleanup Function (Return Value)**: The function returned by `useEffect` is the cleanup mechanism. It ensures that `window.removeEventListener('resize', handleResize)` is called when the component is removed from the DOM. This prevents memory leaks and stops listeners from firing on unmounted components.
3.  **No External Libraries**: This hook relies only on built-in browser APIs (`window.innerWidth`, `window.innerHeight`) and standard React hooks (`useState`, `useEffect`).

191 t/s, 759 tokens, 4s
