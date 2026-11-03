# Qwen Qwen3 14B
Model: qwen_qwen3-14b
Test: Hook Window Size
Created: 11/02/2026, 02:05:02 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is a well-structured implementation of the `useWindowSize` custom React hook in **TypeScript**, designed for use with **React 18+** hooks only. It returns an object containing the current window dimensions (`width` and `height`) and updates automatically on window resize, while also ensuring proper cleanup.

---

### ✅ Features

- Returns `{ width: number; height: number }`
- Updates dynamically when the browser window is resized
- Handles server-side rendering (SSR) gracefully by checking for the presence of `window`
- Properly cleans up event listeners to avoid memory leaks

---

### 🧩 Implementation

```tsx
import { useState, useEffect } from 'react';

/**
 * Custom hook that returns current window dimensions.
 *
 * @returns An object with `width` and `height` properties representing the current window size.
 */
const useWindowSize = (): { width: number; height: number } => {
  // Initialize state with default values in case of SSR
  const [size, setSize] = useState({
    width: typeof window === 'undefined' ? 0 : window.innerWidth,
    height: typeof window === 'undefined' ? 0 : window.innerHeight
  });

  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Function to update state on resize
      const handleResize = () => {
        setSize({
          width: window.innerWidth,
          height: window.innerHeight
        });
      };

      // Add event listener for resize
      window.addEventListener('resize', handleResize);

      // Cleanup function to remove the event listener
      return () => {
        window.removeEventListener('resize', handleResize);
      };
    }
  }, []); // Empty dependency array ensures this runs only once

  return size;
};

export default useWindowSize;
```

---

### 📌 Usage Example

```tsx
import React from 'react';
import useWindowSize from './useWindowSize';

const WindowSizeDisplay: React.FC = () => {
  const { width, height } = useWindowSize();

  return (
    <div>
      <p>Window Width: {width}px</p>
      <p>Window Height: {height}px</p>
    </div>
  );
};

export default WindowSizeDisplay;
```

---

### 📦 Notes

- This hook is **client-side only** and assumes it will be used in a browser environment.
- It gracefully handles **server-side rendering (SSR)** by checking if `window` exists before accessing its properties, preventing runtime errors during SSR.
- The use of `useEffect` with an empty dependency array ensures that the event listener is added once when the component mounts and removed once when it unmounts.

---

This implementation adheres to best practices in React 18+ and TypeScript while ensuring robustness across different environments.

11 t/s, 3409 tokens, 316s
