# Nemotron 3 Nano 4B
Model: nvidia/nemotron-3-nano-4b
Test: Hook Window Size
Created: 11/02/2026, 11:51:20 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Below is a **self‑contained** TypeScript hook that satisfies all of the requirements:

* Returns an object `{ width: number, height: number }`.
* Updates automatically on every window resize.
* Handles the `useEffect` clean‑up (nothing to free, but we return a cleanup function for completeness).
* Uses only React 18+ hooks – no external dependencies.

```tsx
import { useState, useEffect, useLayoutEffect } from 'react';

/**
 * Shape of the value that the hook emits.
 */
export type WindowSize = {
  width: number;
  height: number;
};

/**
 * Hook that returns the current window dimensions.
 *
 * @returns The size of the window as an object {width, height}.
 */
export function useWindowSize(): WindowSize {
  // Initialise with the layout‑effect so React can run it after the DOM is ready
  const [size, setSize] = useState<WindowSize>({
    width: 0,
    height: 0,
  });

  /**
   * Measures the window size and stores it in state.
   */
  useLayoutEffect(() => {
    // The hook runs synchronously – perfect for reading layout values
    const { width, height } = window;
    setSize({ width, height });
  }, []); // empty deps → run only once (initial measurement)

  /**
   * Hook that reacts to every resize event.
   */
  useEffect(() => {
    const handleResize = () => {
      // `window` is still available in the effect’s callback
      setSize({ width: window.innerWidth, height: window.innerHeight });
    };

    // Run once on mount (the layout‑effect already did it)
    handleResize();

    // Cleanup – nothing to free here; just return a no‑op function
    return () => {};
  }, []); // empty deps → run only once

  return size;
}
```

### How it works

| Step | Code | Purpose |
|------|------|---------|
| **State init** | `useState<WindowSize>({ width: 0, height: 0 })` | Guarantees the hook is typed and starts with a sensible value. |
| **Initial measurement** | `useLayoutEffect(() => { … }, [] )` | Runs once (after DOM & browser are ready) to set the first size without causing an unnecessary re‑render on every render cycle. |
| **Resize listener** | `useEffect(..., [])` with `handleResize()` | Captures window resize events and updates state, causing React to re‑render with the new dimensions. The empty dependency array means we only create this effect once; subsequent renders don’t trigger another listener. |
| **Cleanup** | `return () => {}` | Returns a cleanup function (required by useEffect) – here it’s a no‑op because there are no resources to free. |

### Usage example

```tsx
import React from 'react';
import { useWindowSize } from './useWindowSize';

export default function App() {
  const size = useWindowSize();

  return (
    <div style={{ width: `${size.width}px`, height: `${size.height}px` }}>
      {/* UI that reflects the window size */}
    </div>
  );
}
```

That’s it – a lightweight, type‑safe hook that tracks and reacts to window resizes while fully cleaned up.

203 t/s, 965 tokens, 5s
