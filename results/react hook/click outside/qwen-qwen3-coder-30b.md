# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: Hook Click Outside
Created: 11/03/2026, 02:57:27 AM
Exported from: LM Studio (via test script)
Context unknown

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

Here's a production-ready `useClickOutside` React hook implementation in TypeScript:

```typescript
import { useRef, useEffect } from 'react';

type ClickOutsideHandler = (event: MouseEvent | TouchEvent) => void;

function useClickOutside<T extends HTMLElement>(
  ref: React.RefObject<T>,
  callback: () => void
): void {
  const callbackRef = useRef(callback);
  
  // Update the ref to ensure we always have the latest callback
  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  useEffect(() => {
    // Skip if ref is null or element not yet mounted
    if (!ref.current) return;

    const handleClickOutside: ClickOutsideHandler = (event) => {
      // Check if the click target is outside the referenced element
      // Using contains() to check if the event target is a descendant of the ref element
      if (!ref.current?.contains(event.target as Node)) {
        callbackRef.current();
      }
    };

    // Use mousedown and touchstart for better mobile support
    // We listen to both to cover all interaction types
    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('touchstart', handleClickOutside);

    return () => {
      // Clean up event listeners with the exact same functions that were added
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('touchstart', handleClickOutside);
    };
  }, [ref]);
}

export default useClickOutside;
```

This implementation:

1. Uses `mousedown` and `touchstart` events for better mobile support
2. Properly checks if the click/touch target is outside using `contains()` method
3. Handles callback updates with a ref to ensure we always have the latest callback function
4. Adds event listeners only once per mount using `useEffect`
5. Cleans up event listeners properly with the exact same functions that were added
6. Handles edge cases like null refs or unmounted elements
7. Is fully typed with TypeScript generics for type safety
8. Follows React best practices and is production-ready

The hook listens to both mouse and touch events to ensure it works correctly on all device types, and uses `contains()` to properly detect when a click occurs outside the referenced element rather than relying on coordinate checks.

61 t/s, 471 tokens, 8s
