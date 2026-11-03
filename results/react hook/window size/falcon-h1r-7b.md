# Falcon H1R 7B
Model: falcon-h1r-7b
Test: Hook Window Size
Created: 11/02/2026, 12:30:27 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Below is a **stand‑alone TypeScript hook** that follows the React 18+ functional‑hook model, returns an object with the current window width and height, automatically updates on every resize event, and cleans up the listener when the component unmounts or when you manually detach it.

```tsx
// useWindowSize.ts
import { useEffect, useState } from "react";

/**
 * Returns the current window dimensions as an object:
 *   { width: number; height: number }
 *
 * The values are updated automatically whenever the browser window is resized.
 * Cleanup of the resize listener happens when the component unmounts or its
 * parent removes it from React’s tree.
 */

type WindowSize = { width: number; height: number };

/**
 * Hook signature
 */
export const useWindowSize = (): WindowSize => {
  // State that holds the latest size values.
  const [size, setSize] = useState<WindowSize>({
    width: window.innerWidth,
    height: window.innerHeight,
    // Using innerWidth/innerHeight gives the viewport size; you could also use screen.width/height for device‑wide dimensions.
  });

  // Attach a resize listener once after mount. The empty dependency array means this effect runs only on mount.
  useEffect(() => {
    const handler = () => {
      // Update the state whenever the window is resized.
      setSize({ width: window.innerWidth, height: window.innerHeight });
    };

    // Register the listener with the global `window`.
    window.addEventListener("resize", handler);

    // Return a cleanup function that removes the listener when the component unmounts.
    return () => {
      window.removeEventListener("resize", handler);
    };
  }, []); // no external deps

  // `size` is returned on every render, so it reflects the latest values.
  return size;
};
```

### How it works

| Step | Explanation |
|------|-------------|
| **1️⃣ State** – We keep the dimensions in a piece of state (`size`). This ensures that every time we call `setSize`, React schedules a re‑render with the new values. |
| **2️⃣ Effect** – A single effect hook attaches an event listener for the `"resize"` event on the global window. It runs once after mount because its dependency array is empty. |
| **3️⃣ Handler** – When the browser fires a resize, we update state with the new viewport dimensions (`window.innerWidth` / `window.innerHeight`). This triggers an immediate re‑render of any component using the hook. |
| **4️⃣ Cleanup** – The effect returns a cleanup function that removes the listener when the component is unmounted, preventing memory leaks. No extra cleanup is needed for intermediate renders because there’s only one listener. |

### Usage example

```tsx
// SizeDisplay.tsx
import React from "react";
import { useWindowSize } from "./useWindowSize";

export const SizeDisplay: React.FC = () => {
  const size = useWindowSize();

  // Optional: add a debounce to avoid excessive renders if you care about performance.
  // You could replace the handler with setTimeout(() => setSize(...), delay).

  return (
    <div style={{ background: "#fafafa", padding: "1rem" }}>
      <h2>Current window size:</h2>
      <p>{size.width} × {size.height}</p>
    </div>
  );
};
```

Mount the component in your app and you’ll see the numbers update instantly whenever you drag the browser edges or change device orientation on a mobile device.

---

#### Why not use `window.onresize` directly?

* **Lifetime safety** – Adding/removing listeners manually is easy to forget, leading to leaks. The effect‑based approach guarantees cleanup.
* **React integration** – Updating state inside the event handler ensures a clean React reconciliation cycle instead of reading values on render (which would force a full re‑render for every resize).

---

#### Optional enhancements

If you want to throttle updates (e.g., limit them to once per 100 ms), replace the simple handler with a debounced one:

```ts
useEffect(() => {
  const handler = () => {
    clearTimeout(timer);
    // schedule update after delay...
  };
  // set up timer, cleanup both listener and timer.
}, []);
```

But the minimal version above already satisfies the core requirements: it’s a pure React hook, works with React 18+, uses only built‑in hooks, and handles cleanup correctly. Happy coding! 🚀

96 t/s, 3578 tokens, 37s
