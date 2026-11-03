# Qwen2.5 Coder 1.5B Instruct
Model: qwen2.5-coder-1.5b-instruct
Test: Hook Window Size
Created: 11/02/2026, 11:30:21 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```typescript
import { useEffect, useState } from 'react';

function useWindowSize(): { width: number; height: number } {
    const [windowSize, setWindowSize] = useState({ width: window.innerWidth, height: window.innerHeight });

    useEffect(() => {
        function handleResize() {
            setWindowSize({
                width: window.innerWidth,
                height: window.innerHeight
            });
        }

        // Add event listener for resize
        window.addEventListener('resize', handleResize);

        // Cleanup function to remove the event listener when component unmounts
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []); // Empty dependency array ensures this effect runs only once

    return { width: windowSize.width, height: windowSize.height };
}

export default useWindowSize;
```

In this solution, we create a custom React hook called `useWindowSize`. It uses the `useState` hook to keep track of the current window dimensions. The `useEffect` hook is used to add an event listener for the `resize` event on the window object. When the window is resized, the `handleResize` function updates the state with the new dimensions.

The cleanup function in the `useEffect` returns a function that removes the `resize` event listener when the component unmounts, ensuring that the event listener is removed properly to avoid memory leaks. The hook is then exported for use in other components.

297 t/s, 293 tokens, 1s
