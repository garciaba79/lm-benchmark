# Gemma 4 E4B
Model: google/gemma-4-e4b
Test: Hook Window Size
Created: 11/03/2026, 12:38:07 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is the implementation for the `useWindowSize` hook in TypeScript using modern React hooks, ensuring proper cleanup.

### `useWindowSize.ts`

```tsx
import { useState, useEffect } from 'react';

/**
 * Defines the structure for the window size object returned by the hook.
 */
export interface WindowSize {
  width: number;
  height: number;
}

/**
 * A custom React hook that returns the current dimensions of the browser window.
 * It automatically updates whenever the window is resized.
 *
 * @returns {WindowSize} An object containing the current width and height.
 */
export const useWindowSize = (): WindowSize => {
  // Initialize state with the current window dimensions
  const [size, setSize] = useState<WindowSize>(() => ({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  }));

  useEffect(() => {
    // Handler function that updates the state with new dimensions
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Add event listener for resizing
    window.addEventListener('resize', handleResize);

    // Call handler immediately to set the correct size on mount (important if component renders before resize)
    handleResize();

    // Cleanup function: This runs when the component unmounts or before the effect runs again.
    return () => {
      window.removeEventListener('resize', handleResize);
      // Optional: Clean up any other listeners if they were added
    };
  }, [/* Empty dependency array means this effect only runs once on mount and cleans up on unmount */]);

  return size;
};
```

### Explanation and Usage Example

#### Key Concepts Used:

1.  **`useState<WindowSize>`**: We use TypeScript generics to strongly type the state, ensuring `size` is always `{ width: number, height: number }`.
2.  **Lazy Initialization (`() => ({...})`)**: We pass a function to `useState`. This function runs only on the initial render, which is efficient. Crucially, we check `typeof window !== 'undefined'` to ensure this hook works correctly during Server-Side Rendering (SSR) environments (like Next.js), preventing runtime errors when `window` doesn't exist.
3.  **`useEffect`**: This hook manages side effects—in this case, listening to browser events.
4.  **Event Listener Setup**: We add the `resize` event listener using `window.addEventListener('resize', handleResize)`.
5.  **Cleanup (`return () => { ... }`)**: The function returned from `useEffect` is the cleanup mechanism. It *must* remove the event listener (`window.removeEventListener`) to prevent memory leaks when the component unmounts.

---

### Example Usage Component

Here is how you would use this hook in another React component:

```tsx
import React from 'react';
import { useWindowSize } from './useWindowSize'; // Adjust path as necessary

const WindowDimensionsDisplay: React.FC = () => {
  // Simply call the custom hook
  const size = useWindowSize();

  return (
    <div style={{ 
        padding: '20px', 
        border: '1px solid #ccc', 
        borderRadius: '8px',
        textAlign: 'center'
      }}>
      <h1>Window Size Tracker</h1>
      <p>Current Width: <strong>{size.width} px</strong></p>
      <p>Current Height: <strong>{size.height} px</strong></p>
      <p style={{ marginTop: '20px', fontSize: 'small', color: '#666' }}>
        Resize your browser window to see the dimensions update in real-time.
      </p>
    </div>
  );
};

export default WindowDimensionsDisplay;
```

144 t/s, 879 tokens, 6s
