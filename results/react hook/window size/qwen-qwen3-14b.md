# Qwen3 14B
Model: qwen/qwen3-14b
Test: Hook Window Size
Created: 11/03/2026, 01:11:22 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a React hook written in **TypeScript** called `useWindowSize` that returns the current window dimensions as an object `{ width: number, height: number }`. It automatically updates on window resize and properly handles cleanup using React 18+ hooks:

```tsx
import { useState, useEffect } from 'react';

type WindowSize = {
  width: number;
  height: number;
};

function useWindowSize(): WindowSize {
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

    window.addEventListener('resize', handleResize);

    // Cleanup on unmount
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty dependency array so this runs only once

  return windowSize;
}

export default useWindowSize;
```

### ✅ Features:
- **TypeScript** typing ensures type safety.
- **Automatic resizing** is handled via `useEffect`.
- **Cleanup** is done properly with the return function inside `useEffect`.
- It’s fully **compatible with React 18+** and uses only built-in hooks.

### 🔍 Usage Example:

```tsx
import { useWindowSize } from './useWindowSize';

function App() {
  const { width, height } = useWindowSize();

  return (
    <div>
      <p>Window size: {width} x {height}</p>
    </div>
  );
}
```

Let me know if you want to add a fallback or support for SSR!

80 t/s, 354 tokens, 4s
