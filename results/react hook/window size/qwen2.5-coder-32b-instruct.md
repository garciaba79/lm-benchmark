# Qwen2.5 Coder 32B Instruct
Model: qwen2.5-coder-32b-instruct
Test: Hook Window Size
Created: 11/03/2026, 03:41:08 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Certainly! Below is a TypeScript implementation of the `useWindowSize` custom hook in React using React 18+ hooks:

```typescript
import { useState, useEffect } from 'react';

interface WindowSize {
  width: number;
  height: number;
}

const useWindowSize = (): WindowSize => {
  // Initialize state with current window dimensions
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    // Handler to call on window resize
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Add event listener for window resize
    window.addEventListener('resize', handleResize);

    // Call handler right away so state gets updated with initial window size
    handleResize();

    // Remove event listener on cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty array ensures that effect is only run on mount and unmount

  return windowSize;
};

export default useWindowSize;
```

### Explanation:
1. **State Initialization**:
   - The `useState` hook initializes the `windowSize` state with the current dimensions of the window using `window.innerWidth` and `window.innerHeight`.

2. **Effect Hook**:
   - The `useEffect` hook is used to add an event listener for the `resize` event on the window.
   - The `handleResize` function updates the `windowSize` state whenever the window is resized.

3. **Immediate Invocation**:
   - The `handleResize` function is called immediately after adding the event listener to ensure that the initial size is captured and stored in the state.

4. **Cleanup**:
   - A cleanup function is returned from the effect hook, which removes the event listener when the component unmounts or if the dependencies of the effect change (though in this case, there are no dependencies).

5. **Return Value**:
   - The hook returns an object containing the current `width` and `height` of the window.

This custom hook can be used in any functional component to get the current window dimensions and automatically update when the window is resized:

```typescript
import React from 'react';
import useWindowSize from './useWindowSize';

const MyComponent: React.FC = () => {
  const { width, height } = useWindowSize();

  return (
    <div>
      <p>Window Width: {width}px</p>
      <p>Window Height: {height}px</p>
    </div>
  );
};

export default MyComponent;
```

This component will display the current window dimensions and update them automatically whenever the window is resized.

6 t/s, 570 tokens, 91s
