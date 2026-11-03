# GPT-OSS 20B
Model: openai/gpt-oss-20b
Test: Hook Window Size
Created: 11/03/2026, 01:18:48 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Below is a minimal, type‑safe implementation of `useWindowSize` that works with **React 18** (or newer).  
It returns an object `{ width: number; height: number }`, updates on every resize, and cleans up the listener when the component unmounts.

```tsx
import { useState, useEffect } from 'react';

/**
 * Hook that tracks the current browser window size.
 *
 * @returns {{width: number; height: number}} The width and height of the viewport.
 */
export function useWindowSize(): { width: number; height: number } {
  // Helper to get the current dimensions
  const getSize = () => ({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  // State that holds the size – initialise with the current values
  const [size, setSize] = useState<{ width: number; height: number }>(getSize);

  useEffect(() => {
    // Resize handler updates state
    const handleResize = () => setSize(getSize());

    // Register listener
    window.addEventListener('resize', handleResize);

    // Call once to catch any size changes that happened before the effect ran
    handleResize();

    // Cleanup on unmount
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty deps: run only on mount/unmount

  return size;
}
```

### How to use it

```tsx
import { useWindowSize } from './useWindowSize';

function MyComponent() {
  const { width, height } = useWindowSize();

  return (
    <div>
      Window size: {width} × {height}
    </div>
  );
}
```

### Why this works

1. **State** – `size` holds the current dimensions and triggers a re‑render when it changes.
2. **Effect** – registers a single `resize` listener on mount, updates state on each event, and removes the listener on unmount (cleanup).
3. **TypeScript** – the return type is explicitly declared (`{ width: number; height: number }`) ensuring full type safety throughout your component tree.
4. **No external dependencies** – only React built‑in hooks are used.

Feel free to tweak the initial values or add debounce/throttle logic if you want to reduce the frequency of updates.

200 t/s, 539 tokens, 3s
