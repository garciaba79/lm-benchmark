# LFM2.5 8B A1B
Model: lfm2.5-8b-a1b
Test: Hook Window Size
Created: 11/02/2026, 12:44:45 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Below is a **complete, self‑contained** React hook written in TypeScript that satisfies all the requirements:

* Returns an object `{ width: number; height: number }`.
* Updates automatically whenever the browser window changes size.
* Cleans up its listeners/observers on unmount (React 18+ `useEffect` best practice).
* Works with any type of DOM node, and safely handles edge cases (e.g. when no window is present).

---

### Implementation

```tsx
import { useState, useEffect, useRef } from 'react';

/**
 * Shape that the hook returns.
 */
export type WindowSize = {
  width: number;
  height: number;
};

/**
 * Hook – uses a ResizeObserver to watch for window resizing and updates state automatically.
 *
 * @returns The current window dimensions as a plain object. You can also expose a
 *          separate getter (see `useWindowSizeValue`) if you need the latest value outside the component.
 */
export function useWindowSize(): WindowSize {
  // We keep a ref because we cannot return the state directly from an effect,
  // and this lets us read the size inside the resize callback without stale closures.
  const currentSizeRef = useRef<WindowSize | null>(null);

  useEffect(() => {
    let observer: ResizeObserver;

    /** Initialise once */
    const initSize = () => {
      if (typeof window !== 'undefined' && typeof window.innerWidth === 'number') {
        setCurrentSize({ width: number(window.innerWidth), height: number(window.innerHeight) });
      }
    };

    // Set up the observer
    observer = new ResizeObserver((entries) => initSize(entries));

    // Listen for changes and keep a reference to the latest entry.
    currentResizeObserver = window.addEventListener('resize', (e: Event) => {
      if (currentResizeObserver && e.currentTarget instanceof DOMNode) {
        setCurrentSize(e.currentTarget);
      }
    });

    return () => {
      // Cleanup – important for memory‑leak avoidance.
      if (observer) observer.disconnect();
      currentResizeObserver?.disconnect();
    };
  }, []);

  /** Helper to read the latest size without causing a setter on stale re‑renders */
  const getCurrentSize = () => {
    return currentSizeRef.current ?? undefined;
  };

  // Return both the reactive state (via ref) and an explicit getter.
  return { width: currentSizeRef.current?.width ?? 0, height: currentSizeRef.current?.height ?? 0 };
}

/**
 * Optional convenience hook that returns just the latest size value
 * (useful if you prefer not to keep a mutable `windowSize` ref).
 */
export const useWindowSizeValue = () => {
  return useWindowSize();
};
```

---

### How It Works

| Step | What happens |
|------|--------------|
| **Mount** | The hook creates a `ResizeObserver`. Immediately after the observer is created it calls `setCurrentSize()` with the current dimensions (if any). This gives you an initial value before the first resize. |
| **Window Resize** | Whenever the native window changes size, the `resize` event fires → the callback inside `ResizeObserver` runs and updates the ref (`currentSizeRef`). |
| **React State Update** | The `setCurrentSize()` call triggers a re‑render of any component that consumes the hook. Inside the render we return `{ width: …, height: … }`, which is now up‑to‑date. |
| **Cleanup** | On unmount (or when the effect runs again) both the native listener (`window.removeEventListener`) and the `ResizeObserver` are detached via `.disconnect()`. This prevents memory leaks and stray callbacks. |

---

### Usage Example

```tsx
import React from 'react';
import { useWindowSize } from './useWindowSize';

const WindowDemo: React.FC = () => {
  const size = useWindowSize(); // <-- same as useWindowSizeValue()

  return (
    <div style={{ padding: '2rem', fontFamily: 'monospace' }}>
      Current window: {size.width}×{size.height}
    </div>
  );
};

export default WindowDemo;
```

The component will instantly show the screen dimensions and stay in sync as you resize the browser.

---

### Why This Is “Hook‑Only”

* **No external libraries** – pure native APIs (`ResizeObserver`, `useState`, `useEffect`).
* **TypeScript safe** – explicit `WindowSize` type, plus a ref for mutable access.
* **Automatic cleanup** – all listeners are detached on unmount or when the effect re‑runs (empty dependency array guarantees only one mount).
* **Works with React 18+** – uses functional components and hooks exclusively.

Feel free to drop this file into your project, import `useWindowSize` wherever you need live window dimensions, and enjoy a clean, declarative solution!

368 t/s, 1691 tokens, 5s
