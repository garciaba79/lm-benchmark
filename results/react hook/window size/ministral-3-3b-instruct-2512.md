# Ministral 3 3B Instruct 2512
Model: ministral-3-3b-instruct-2512
Test: Hook Window Size
Created: 11/02/2026, 11:47:07 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's a `useWindowSize` React hook for TypeScript that uses React 18+ features (including the new `useEffect` API with dependency array optimization) to track window dimensions:

```typescript
import { useState, useEffect } from 'react';

type WindowSize = {
  width: number;
  height: number;
};

const useWindowSize = (): WindowSize => {
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  // Only run effect once on initial render
  useEffect(() => {
    function handleResize(): void {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    // Add event listener for window resize
    window.addEventListener('resize', handleResize);

    // Cleanup the event listener on component unmount
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty dependency array ensures this runs only once

  return windowSize;
};

export default useWindowSize;
```

### Key Features:
1. **Type Safety**: Uses TypeScript to properly type the returned dimensions
2. **Automatic Updates**: Listens to `resize` events and updates state when window changes
3. **Cleanup**: Properly removes the event listener when component unmounts
4. **Initial Value**: Sets initial values from `window.innerWidth`/`innerHeight`
5. **React 18+ Compliance**:
   - Uses the new empty dependency array for cleanup
   - Doesn't use any external libraries

### Usage Example:
```typescript
import React from 'react';
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

export default MyComponent;
```

This implementation follows React best practices for performance and memory management while providing the exact functionality requested.

210 t/s, 455 tokens, 2s
