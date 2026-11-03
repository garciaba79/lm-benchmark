# Gemma 4 12B QAT
Model: google/gemma-4-12b-qat
Test: Hook Window Size
Created: 11/02/2026, 01:12:39 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

To create this hook, we will use the `useState` hook to store the dimensions and the `useEffect` hook to attach and detach the `resize` event listener.

Here is the production-ready implementation:

```typescript
import { useState, useEffect } from 'react';

/**
 * A custom hook that returns the current window dimensions.
 * Updates automatically when the window is resized.
 * 
 * @returns An object containing the current width and height of the window.
 */
export const useWindowSize = () => {
  // Initialize state with the current window dimensions
  // Using a function in useState ensures we only read window.innerWidth/Height once on mount
  const [windowSize, setWindowSize] = useState(() => ({
    width: window.innerWidth,
    height: window.innerHeight,
  }));

  useEffect(() => {
    // Handler to update state
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Add event listener
    window.addEventListener('resize', handleResize);

    // Cleanup: Remove event listener when component unmounts
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return windowSize;
};
```

### Key Features of this Implementation:

1.  **Lazy Initial State:** By passing a function to `useState`, we ensure that `window.innerWidth` is only accessed during the initial render. This is a best practice for hooks that interact with the DOM/Window.
2.  **Cleanup:** The return function in `useEffect` ensures that the event listener is removed when the component is destroyed, preventing memory leaks.
3.  **Type Safety:** It uses TypeScript to ensure the returned object strictly follows the `{ width: number, height: number }` structure.
4.  **Performance:** It uses the native `resize` event which is the standard way to detect window changes in React 18.

### Example Usage:

```tsx
import React from 'react';
import { useWindowSize } from './useWindowSize';

const ResponsiveComponent = () => {
  const { width, height } = useWindowSize();

  return (
    <div>
      <h1>Window Dimensions</h1>
      <p>Width: {width}px</p>
      <p>Height: {height}px</p>
      {width < 768 ? (
        <p>You are on a mobile device!</p>
      ) : (
        <p>You are on a desktop device!</p>
      )}
    </div>
  );
};

export default ResponsiveComponent;
```

### Note on SSR (Next.js / Remix):
If you are using a Server-Side Rendering (SSR) framework, `window` is not defined on the server. To prevent errors, you can add a check inside the hook or use a `useEffect` to initialize the state:

```typescript
// Add this inside the hook if using SSR
useEffect(() => {
  const handleResize = () => {
    setWindowSize({ width: window.innerWidth, height: window.innerHeight });
  };
  window.addEventListener('resize', handleResize);
  handleResize(); // Trigger initial sync
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

94 t/s, 742 tokens, 8s
