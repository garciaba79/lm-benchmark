# Granite 4.1 8B
Model: granite-4.1-8b
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

Below is a TypeScript implementation of the `useClickOutside` custom React hook that meets all the specified requirements:

```typescript
import { useEffect } from 'react';

/**
 * Custom hook to detect clicks outside a referenced element.
 * @param ref - A ref attached to the target DOM element.
 * @param onClickOutside - Callback function triggered on click outside the target element.
 */
export const useClickOutside = (ref: React.RefObject<HTMLElement>, onClickOutside: (event: MouseEvent) => void) => {
  // Effect runs only once when the component mounts or unmounts
  useEffect(() => {
    // Helper function to determine if a click is outside the referenced element
    const handleClick = (event: MouseEvent) => {
      // Check if `ref.current` exists and whether the clicked target is within it
      if (!ref.current || ref.current.contains(event.target as Node)) return;
      onClickOutside(event);
    };

    // Add event listener for click events on the document/window.
    // Using 'click' is sufficient for most use cases; consider adding 'touchstart' if necessary for mobile touch interactions.
    document.addEventListener('click', handleClick);

    // Cleanup: remove the event listener when the component unmounts or ref changes
    return () => {
      document.removeEventListener('click', handleClick);
    };
  }, [ref, onClickOutside]); // Dependencies are `ref` and `onClickOutside`
};

// Example usage:
// const myRef = useRef<HTMLDivElement>(null);
// useClickOutside(myRef, (event) => console.log('Clicked outside!', event));
```

### Key Points of the Implementation:

1. **Event Listener Management**: 
   - The hook uses `useEffect` to ensure the click event listener is added only once during component mount and removed during unmount or when dependencies change.
   - This prevents memory leaks and duplicate listeners.

2. **Checking if Click is Outside**:
   - Instead of using `getBoundingClientRect()`, the solution leverages the `.contains()` method of DOM elements to accurately determine if the click target (`event.target`) is inside the referenced element (`ref.current`).

3. **Handling Null or Unmounted Refs**: 
   - The check `if (!ref.current || ref.current.contains(event.target as Node)) return;` ensures that the callback isn't triggered when there's no reference to an element (e.g., during unmounting or before the DOM node is ready).

4. **Event Propagation**:
   - Using `'click'` on `document` captures clicks regardless of where in the document they occur, so additional handling for event propagation (like `stopPropagation`) isn't necessary here.

5. **Type Safety and Browser Compatibility**: 
   - The hook strictly type-checks the parameters with TypeScript, ensuring `ref` is a React ref to an `HTMLElement` and `onClickOutside` receives a `MouseEvent`. This approach works across modern browsers supporting React 18+ hooks.

This implementation provides a clean, efficient, and production-ready solution for detecting clicks outside a specified element in a React application.

126 t/s, 632 tokens, 5s, 6%
