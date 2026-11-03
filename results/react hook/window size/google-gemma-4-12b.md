# Gemma 4 12B
Model: google/gemma-4-12b
Test: Hook Window Size
Created: 11/03/2026, 01:02:26 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

To create this hook, we will use `useState` to store the dimensions and `useEffect` to attach/detach the event listener.

Here is the production-ready implementation:

```typescript
import { useState, useEffect } from 'react';

/**
 * A custom hook that returns the current window width and height.
 * Updates automatically whenever the window is resized.
 */
export function useWindowSize(): { width: number; height: number } {
  // Initialize state with current window dimensions
  const [windowSize, setWindowSize] = useState({
    width: (window as Window).innerWidth || 0,
    height: (window as Window).innerHeight || 0,
  });

  useEffect(() => {
    // Handler to update state when the window is resized
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Add event listener
    window.addEventListener('resize', handleResize);

    // Cleanup: Remove listener when component unmounts
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
}
```

### Key Features of this implementation:
1.  **TypeScript Support**: It explicitly defines the return type as `{ width: number; height: number }`.
2.  **Initial State**: It calculates the dimensions immediately on mount so the component doesn't start with `0` values (useful for SSR-friendly logic or initial paint).
3.  **Memory Management**: The `useEffect` cleanup function ensures that the `resize` listener is removed when the component unmounts, preventing memory leaks.
4.  **React 18+ Compatible**: Uses standard hooks and follows standard React lifecycle patterns.

### Example Usage:

```tsx
import React from 'react';
import { useWindowSize } from './hooks/useWindowSize'; // adjust path accordingly

const ResponsiveComponent: React.FC = () => {
  const { width, height } = useWindowSize();

  return (
    <div>
      <h1>Window Dimensions</h1>
      <p>Width: {width}px</p>
      <p>Height: {height}px</p>
      
      {width < 768 ? (
        <p>You are on a mobile device.</p>
      ) : (
        <p>You are on a desktop device.</p>
      )}
    </div>
  );
};

export default ResponsiveComponent;
```

### Performance Note:
If you find yourself using this hook in many components simultaneously, it will cause all components using the hook to re-render every time the window is resized. If performance becomes an issue, you can wrap the `handleResize` logic in a **Context Provider** so only one listener exists for the entire application.

82 t/s, 623 tokens, 8s
