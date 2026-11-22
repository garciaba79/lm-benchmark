# Gemma 4 26B A4B QAT
Model: google/gemma-4-26b-a4b-qat
Test: Hook Window Size
Created: 11/22/2026, 03:09:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is a robust, production-ready implementation of the `useWindowSize` hook in TypeScript.

```typescript
import { useState, useEffect } from 'react';

interface WindowSize {
  width: number;
  height: number;
}

/**
 * A hook that returns the current window dimensions.
 * Updates automatically when the window is resized.
 */
export const useWindowSize = (): WindowSize => {
  // Initialize state with undefined to prevent SSR (Server Side Rendering) mismatch
  // If using Next.js or Remix, this ensures the first render matches the server.
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  useEffect(() => {
    // Function to update state with current window dimensions
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Add event listener
    window.addEventListener('resize', handleResize);

    // Call handler immediately to ensure state is synced on mount
    handleResize();

    // Cleanup function to remove listener when component unmounts
    return () => window.removeEventListener('resize', handleResize);
  }, []); // Empty dependency array means this runs once on mount

  return windowSize;
};
```

### Key Features of this Implementation:

1.  **TypeScript Interfaces**: Uses a `WindowSize` interface to ensure type safety for the returned object.
2.  **SSR Safety**: It checks `typeof window !== 'undefined'`. This prevents the application from crashing if you use this hook in a framework like **Next.js**, where the code might execute on the server where `window` does not exist.
3.  **Memory Leak Prevention**: It returns a cleanup function `window.removeEventListener` inside `useEffect`. This is crucial to prevent memory leaks when the component using the hook is destroyed.
4.  **React 18 Ready**: Uses standard `useState` and `useEffect` patterns compatible with React 18's Concurrent Mode.
5.  **Immediate Sync**: It calls `handleResize()` inside the `useEffect` to ensure the dimensions are captured immediately upon mounting, even if the window was resized before the component mounted.

### Usage Example:

```tsx
import React from 'react';
import { useWindowSize } from './useWindowSize';

const MyComponent = () => {
  const { width, height } = useWindowSize();

  return (
    <div style={{ padding: '20px' }}>
      <h1>Window Dimensions</h1>
      <p>Width: {width}px</p>
      <p>Height: {height}px</p>
      
      {width < 768 ? (
        <p>📱 You are on a mobile-sized screen.</p>
      ) : (
        <p>💻 You are on a desktop-sized screen.</p>
      )}
    </div>
  );
};

export default MyComponent;
```

### Optimization Note (Throttling/Debouncing)
In a highly complex application where many components use this hook simultaneously, the `resize` event can fire many times per second. If you notice performance issues, you might want to wrap the `handleResize` function in a **debounce** or **throttle** function to limit the number of state updates.

56 t/s, 768 tokens, 14s, 5%
