# Qwen2.5 Coder 14B
Model: qwen/qwen2.5-coder-14b
Test: Hook Window Size
Created: 11/02/2026, 02:10:18 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a TypeScript implementation of the `useWindowSize` hook using React 18+ hooks:

```typescript
import { useState, useEffect } from 'react';

function useWindowSize(): { width: number; height: number } {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    // Add event listener
    window.addEventListener('resize', handleResize);

    // Cleanup function to remove the event listener on component unmount
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty dependency array ensures this effect runs only once after initial render

  return windowSize;
}

export default useWindowSize;
```

This hook initializes state with the current window dimensions and sets up an event listener for the `resize` event. When the window is resized, it updates the state with the new dimensions. The cleanup function returned by `useEffect` removes the event listener when the component unmounts to prevent memory leaks.

To use this hook in a component:

```typescript
import React from 'react';
import useWindowSize from './useWindowSize';

function App() {
  const { width, height } = useWindowSize();

  return (
    <div>
      Window Size:
      <div>Width: {width}px</div>
      <div>Height: {height}px</div>
    </div>
  );
}

export default App;
```

This will display the current window dimensions and update automatically when the window is resized.

77 t/s, 346 tokens, 4s
