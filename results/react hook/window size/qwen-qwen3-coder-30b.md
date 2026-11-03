# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: Hook Window Size
Created: 11/03/2026, 02:58:36 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```typescript
import { useState, useEffect } from 'react';

interface WindowSize {
  width: number;
  height: number;
}

const useWindowSize = (): WindowSize => {
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Add event listener
    window.addEventListener('resize', handleResize);

    // Cleanup function to remove event listener
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return windowSize;
};

export default useWindowSize;
```

This hook works by:

1. **Initial State**: Sets the initial window dimensions using `window.innerWidth` and `window.innerHeight`
2. **Event Listener**: Adds a resize event listener that updates the state whenever the window is resized
3. **Cleanup**: Removes the event listener when the component unmounts to prevent memory leaks
4. **Type Safety**: Uses TypeScript interfaces for proper typing of the returned object
5. **React 18+ Compatibility**: Uses only standard React hooks without any external dependencies

The hook returns an object with `width` and `height` properties that automatically update when the window is resized. The cleanup ensures that event listeners are properly removed, preventing potential memory leaks in long-running applications.

64 t/s, 301 tokens, 5s
