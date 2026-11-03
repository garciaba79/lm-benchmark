# Nvidia NVIDIA Nemotron Nano 9B v2
Model: nvidia_nvidia-nemotron-nano-9b-v2
Test: Hook Window Size
Created: 11/02/2026, 12:52:49 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a well-structured and type-safe implementation of the `useWindowSize` React hook using TypeScript and React 18+ hooks:

```tsx
import { useState, useEffect } from 'react';

/**
 * A custom React hook that returns the current window dimensions as an object.
 * It updates automatically on window resize and cleans up the event listener on unmount.
 */
function useWindowSize(): { width: number; height: number } {
  // Initialize state with the current window dimensions
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  // Add a resize event listener when the component mounts
  useEffect(() => {
    const handleResize = () => {
      // Update state with new dimensions on resize
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Attach the event listener
    window.addEventListener('resize', handleResize);

    // Cleanup: remove the event listener when the component unmounts
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty dependency array ensures this runs only once on mount

  // Return the current window size
  return windowSize;
}

export default useWindowSize;
```

---

### ✅ Key Features:

- **Automatic Updates**: The hook listens for `resize` events and updates the state accordingly.
- **Cleanup**: Properly removes the event listener when the component unmounts to avoid memory leaks.
- **Type Safety**: Uses TypeScript to define the return type as `{ width: number; height: number }`.
- **React 18+ Compatible**: Uses only built-in React hooks (`useState`, `useEffect`) with no external dependencies.

---

### 🧪 Usage Example:

```tsx
import React from 'react';
import useWindowSize from './useWindowSize';

const ResizeObserver = () => {
  const { width, height } = useWindowSize();

  return (
    <div>
      <p>Current window size: {width} × {height}</p>
    </div>
  );
};

export default ResizeObserver;
```

This hook is efficient, clean, and adheres to best practices for React hooks in modern applications.

103 t/s, 2082 tokens, 20s
