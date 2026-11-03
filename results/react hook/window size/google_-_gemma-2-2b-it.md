# Gemma 2 2B Instruct
Model: google_-_gemma-2-2b-it
Test: Hook Window Size
Created: 11/02/2026, 11:31:25 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```typescript
import { useState, useEffect } from 'react';

function useWindowSize(): { width: number; height: number } {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    // Update window size on every resize event
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };
    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize); // Cleanup on unmount
  }, []); // Empty dependency array ensures it runs only once after mount

  return windowSize;
}

export default useWindowSize;
```

**Explanation:**

1. **Import `useState` and `useEffect`:** We need these hooks from React for managing state and side effects respectively.
2. **Create the hook:** The `useWindowSize()` function returns an object with width and height properties, initialized with window dimensions on mount. 
3. **State Management:** `useState` is used to manage the `windowSize` object. It stores the current width and height values.
4. **useEffect for Resizing Handling:**  
   - The `useEffect` hook runs after the component renders, ensuring that it's called only once on mount (empty dependency array). 
   - Inside the effect:
      - A function named `handleResize` is defined to update the `windowSize` state whenever the window size changes.
      -  An event listener for the 'resize' event is added to the window, triggering `handleResize` when the window resizes.
      - The cleanup logic returns a function that removes the event listener on unmount (using `window.removeEventListener`). 

5. **Returning Window Dimensions:** Finally, we return the current `windowSize`.



**How to use it in your component:**

```javascript
import { useState } from 'react';
import { useWindowSize } from './useWindowSize'; // Import the hook

function MyComponent() {
  const windowWidth = useWindowSize(); 
  return (
    <div>
      <h2>Window Width: {windowWidth.width}</h2>
      {/* Use windowWidth for your layout or logic */}
    </div>
  );
}
```



**Key Points:**

- **TypeScript Type Safety:** The `useWindowSize` hook uses TypeScript to ensure type safety, making it more robust and maintainable. 
- **Automatic Updates:** The use of the `useEffect` hook with a cleanup function ensures that the state is correctly updated whenever the window's dimensions change automatically.  
- **React Hooks Only:** We are using only React hooks for this functionality without any external libraries, keeping it simple and lightweight.


Let me know if you have any other questions!

213 t/s, 621 tokens, 3s
