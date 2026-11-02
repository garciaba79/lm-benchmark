# GPT-OSS 20B
Model: openai/gpt-oss-20b
Test: Hook Click Outside
Created: 11/02/2026, 05:51:42 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useClickOutside in TypeScript that takes a ref to an HTMLElement and a callback function. The callback should be called when the user clicks outside the referenced element. Use React 18+ hooks only, no external libraries, and ensure proper event listener cleanup.

Important reminders and tips (double-check these before submitting your final code):
- Think carefully about which event(s) you should listen to: is 'click' always the best choice, or should you consider 'mousedown' or 'touchstart' for better mobile behavior?
- Make sure the check for "outside" uses the correct DOM method to see if the click target is inside or a child of the referenced element.
- Avoid common mistakes: do NOT use getBoundingClientRect() coordinates to check position — that approach is fragile and unnecessary.
- Ensure the event listener is added only once per mount (not on every render) to prevent duplicate listeners.
- The cleanup must properly remove the exact same listener function that was added.
- The hook should return void (nothing) — it performs side-effects only.
- Handle cases where the ref might be null or the element not yet mounted.
- Consider browser event propagation and whether you need to stop propagation in any cases.

Take your time, reason step by step if needed, and make sure your code is clean, type-safe, and production-ready.

> #### 🤖 Assistant

```tsx
/**
 * useClickOutside
 *
 * Calls the supplied callback when a user clicks (or touches) outside of the element
 * referenced by `ref`. The hook is fully type‑safe, uses only React 18 hooks,
 * and cleans up listeners properly.
 */

import { useEffect, useRef } from "react";

type ClickOutsideCallback = () => void;

/**
 * @param ref   A RefObject pointing to the element that should be considered “inside”.
 * @param callback The function to run when a click/touch occurs outside of that element.
 */
export function useClickOutside(
  ref: React.RefObject<HTMLElement>,
  callback: ClickOutsideCallback
): void {
  // Keep the latest callback in a ref so we can call it from the event handler
  // without re‑registering listeners on every render.
  const callbackRef = useRef(callback);
  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  useEffect(() => {
    /**
     * Handles both mouse and touch events. We check if the event target is a
     * descendant of the referenced element. If not, we invoke the stored callback.
     */
    const handleEvent = (event: MouseEvent | TouchEvent): void => {
      // `ref.current` may be null during the initial render or before mounting.
      const node = ref.current;
      if (!node) return;

      // `event.target` is always a Node in both mouse and touch events.
      const target = event.target as Node | null;
      if (!target) return;

      // If the click/touch happened inside the element, do nothing.
      if (node.contains(target)) {
        return;
      }

      // Outside – invoke the callback.
      callbackRef.current();
    };

    // Attach listeners for mouse and touch interactions.
    document.addEventListener("mousedown", handleEvent);
    document.addEventListener("touchstart", handleEvent);

    // Cleanup: remove the exact same listener functions.
    return () => {
      document.removeEventListener("mousedown", handleEvent);
      document.removeEventListener("touchstart", handleEvent);
    };
  }, [ref]); // Only re‑run if the ref itself changes (rare).
}
```

### How it works

1. **Single registration** – The `useEffect` that adds listeners runs only once per mount because its dependency array contains only `ref`.  
2. **Current callback** – We store the latest `callback` in a mutable ref (`callbackRef`) and update it whenever the prop changes, so the event handler always calls the newest function without needing to re‑register listeners.  
3. **Outside detection** – The native DOM method `node.contains(target)` is used; this correctly handles nested children and works for both mouse and touch events.  
4. **Cleanup** – The cleanup function removes *exactly* the same handler functions that were added, preventing leaks or duplicate calls.  

The hook performs a side‑effect only and therefore returns nothing (`void`).

122 t/s, 1004 tokens, 9s, 8%
