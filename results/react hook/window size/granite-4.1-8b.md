# Granite 4.1 8B
Model: granite-4.1-8b
Test: Hook Window Size
Created: 11/02/2026, 12:43:02 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Certainly! Below is a TypeScript implementation of a custom React hook named `useWindowSize`. This hook will return the current dimensions of the browser window (width and height) as an object `{ width: number, height: number }` and will automatically update whenever the window is resized. It properly cleans up event listeners on component unmount using React 18+ hooks.

```typescript
import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook to track the size of the browser window.
 * @returns An object containing the current width and height of the window in pixels.
 */
export const useWindowSize = (): { width: number; height: number } => {
  // State to hold the dimensions
  const [windowSize, setWindowSize] = useState<{ width: number; height: number }>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  // Use useCallback to wrap the resize handler for memoization
  const handleResize = useCallback(() => {
    setWindowSize({
      width: window.innerWidth,
      height: window.innerHeight,
    });
  }, []);

  // useEffect to add and remove event listeners on window resize
  useEffect(() => {
    // Add event listener for window resize
    window.addEventListener('resize', handleResize);

    // Cleanup function to remove the event listener
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [handleResize]);

  return windowSize;
};

// Example usage within a functional component:
/*
import React from 'react';
import { useWindowSize } from './useWindowSize';

const App: React.FC = () => {
  const { width, height } = useWindowSize();

  return (
    <div>
      <p>Window Width: {width}px</p>
      <p>Window Height: {height}px</p>
    </div>
  );
};

export default App;
*/
```

### Explanation:

1. **State Initialization**: The hook initializes a state variable `windowSize` using `useState`, capturing the initial window dimensions (`innerWidth` and `innerHeight`).

2. **Resize Handler**: A resize handler function, wrapped in `useCallback`, updates the `windowSize` state whenever the window is resized.

3. **Effect Hook**: The `useEffect` hook adds an event listener for the 'resize' event on the window object. It also returns a cleanup function that removes this event listener when the component unmounts or when the handler function changes (though in this case, it remains constant).

4. **TypeScript Typing**: The hook is typed to return an object with `width` and `height` properties of type `number`.

5. **No External Libraries**: This implementation relies solely on built-in React hooks and standard JavaScript window properties, adhering to the requirement of not using external libraries.

This custom hook can be easily integrated into any functional component to monitor or react to changes in the browser window size.

125 t/s, 603 tokens, 5s
