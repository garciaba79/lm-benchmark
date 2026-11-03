# Qwen3.5 4B
Model: qwen3.5-4b
Test: Hook Window Size
Created: 11/02/2026, 12:18:42 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is a robust implementation of the `useWindowSize` hook using TypeScript and React 18+ hooks (`useState`, `useEffect`). It includes proper event listener cleanup to prevent memory leaks.

```tsx
import { useState, useEffect } from 'react';

// Define the return type for clarity
interface WindowSize {
  width: number;
  height: number;
}

/**
 * Custom hook to track window dimensions.
 * Updates automatically on resize and cleans up event listeners properly.
 */
export const useWindowSize = (): WindowSize => {
  // Initialize state with current dimensions (or defaults if not available)
  const [size, setSize] = useState<WindowSize>({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  useEffect(() => {
    // Define the resize handler function
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Attach the event listener on mount
    if (typeof window !== 'undefined') {
      window.addEventListener('resize', handleResize);
      
      // Optional: Trigger initial check immediately to ensure state is accurate 
      // before the first render cycle completes.
      handleResize(); 
    }

    // Cleanup function: Remove event listener on unmount or dependency change
    return () => {
      if (typeof window !== 'undefined') {
        window.removeEventListener('resize', handleResize);
      }
    };
  }, []); // Empty dependency array ensures this runs only once on mount

  return size;
};
```

### Usage Example

You can use the hook in any component to access dimensions:

```tsx
import React from 'react';
import { useWindowSize } from './useWindowSize';

const Component = () => {
  const { width, height } = useWindowSize();

  return (
    <div style={{ padding: `${height}px` }}>
      <h1>Window Width: {width}</h1>
      <p>Window Height: {height}</p>
    </div>
  );
};

export default Component;
```

### Key Implementation Details

1.  **State Initialization**: The initial state is set immediately using `window.innerWidth`/`Height`. This prevents a "flash" of incorrect data before the first resize event fires.
2.  **Cleanup (`useEffect`)**: The return function in `useEffect` ensures that `removeEventListener` is called when the component unmounts or dependencies change, preventing memory leaks and potential errors if the listener is still attached to a destroyed window object.
3.  **Type Safety**: A strict TypeScript interface (`WindowSize`) ensures type safety for consumers of this hook.
4.  **Environment Check**: Includes `typeof window !== 'undefined'` checks to ensure compatibility in environments where the browser API might not be available (e.g., Server-Side Rendering setups).

160 t/s, 2063 tokens, 13s
