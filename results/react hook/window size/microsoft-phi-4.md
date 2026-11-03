# Phi 4
Model: microsoft/phi-4
Test: Hook Window Size
Created: 11/03/2026, 01:16:16 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

To create a `useWindowSize` custom hook in TypeScript using React 18+, you can follow these steps:

1. Utilize the `useState`, `useEffect`, and `RefObject` from React to track window dimensions.
2. Set up an event listener for window resizing within `useEffect`.
3. Ensure proper cleanup of the event listener when the component unmounts or dependencies change.

Below is the implementation:

```tsx
import { useState, useEffect } from 'react';

// Define a TypeScript type for the return value
type WindowSize = {
  width: number;
  height: number;
};

const useWindowSize = (): WindowSize => {
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    // Handler to call on window resize
    const handleResize = () => {
      // Set new state with updated window dimensions
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Add event listener for resizing the window
    window.addEventListener('resize', handleResize);

    // Cleanup function to remove the event listener on unmount or dependencies change
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty dependency array ensures this effect runs only once (like componentDidMount)

  return windowSize;
};

export default useWindowSize;
```

### Explanation:

- **State Management**: We initialize the `windowSize` state with the current dimensions using `useState`.
- **Effect Hook**: The `useEffect` hook is used to set up a resize event listener on the window. It calls `handleResize` whenever the window resizes, updating the state.
- **Cleanup**: The return function within `useEffect` handles the removal of the event listener when the component unmounts or dependencies change (although in this case, we have an empty dependency array to ensure it runs once).
  
This hook can be used in any functional component to get the current window size and automatically updates as the window is resized.

81 t/s, 431 tokens, 5s
