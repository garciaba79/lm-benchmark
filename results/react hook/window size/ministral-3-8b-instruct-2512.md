# Ministral 3 8B Instruct 2512
Model: ministral-3-8b-instruct-2512
Test: Hook Window Size
Created: 11/02/2026, 12:47:29 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a `useWindowSize` hook written in TypeScript for React 18+ that returns the current window dimensions (`width` and `height`) and updates them when the window is resized:

```typescript
import { useState, useEffect } from 'react';

const useWindowSize = (): { width: number; height: number } => {
  const [windowSize, setWindowSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  useEffect(() => {
    // Handle initial size
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Add event listener for resize
    window.addEventListener('resize', handleResize);

    // Cleanup function to remove the event listener when component unmounts
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty dependency array means this effect runs once on mount

  return windowSize;
};

export default useWindowSize;
```

### Key Features:
1. **TypeScript Support**: Returns an object with `width` and `height` as numbers.
2. **React 18+ Compatible**: Uses modern hooks (`useState`, `useEffect`).
3. **Server-Side Rendering (SSR) Safe**: Checks for `window` existence to avoid errors on the server.
4. **Cleanup**: Properly removes the event listener when the component unmounts.
5. **No External Dependencies**: Pure React implementation.

### Usage Example:
```typescript
import useWindowSize from './useWindowSize';

const MyComponent = () => {
  const { width, height } = useWindowSize();

  return (
    <div>
      <p>Width: {width}px</p>
      <p>Height: {height}px</p>
    </div>
  );
};
```

### Notes:
- The hook initializes with `window.innerWidth` and `window.innerHeight` on mount.
- It updates the state whenever the window is resized.
- The cleanup function ensures no memory leaks by removing the event listener.

127 t/s, 482 tokens, 4s
