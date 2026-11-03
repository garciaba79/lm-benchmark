# Qwen2.5 Coder 7B Instruct
Model: qwen2.5-coder-7b-instruct
Test: Hook Window Size
Created: 11/02/2026, 12:31:57 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's how you can create a `useWindowSize` hook in TypeScript using React 18+ hooks:

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

        // Cleanup function to remove the event listener when component unmounts
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []); // Empty dependency array means this effect runs only once after the initial render

    return windowSize;
};

export default useWindowSize;
```

### Explanation:

1. **useState**: We initialize `windowSize` with an object containing the current width and height of the window.

2. **useEffect**:
   - The `handleResize` function updates the state whenever the window is resized.
   - We add this event listener in the effect to listen for resize events on the window.
   - A cleanup function is returned from the useEffect, which removes the event listener when the component unmounts.

3. **Empty Dependency Array**: By passing an empty array `[]` as the second argument to `useEffect`, we ensure that this effect runs only once after the initial render of the component.

### Usage:

You can use this hook in any React component like so:

```typescript
import React from 'react';
import useWindowSize from './useWindowSize';

const MyComponent: React.FC = () => {
    const { width, height } = useWindowSize();

    return (
        <div>
            Window Width: {width}px<br />
            Window Height: {height}px
        </div>
    );
};

export default MyComponent;
```

This will display the current window dimensions and update them automatically as you resize your browser window.

145 t/s, 441 tokens, 3s
