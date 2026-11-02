# Mamba Codestral 7B v0.1
Model: mamba-codestral-7b-v0.1
Test: Hook Click Outside
Created: 11/02/2026, 05:51:42 AM
Exported from: LM Studio (via test script)
Context 32K

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

```typescript
import { useEffect } from 'react';

function useClickOutside<T extends HTMLElement = HTMLElement>(ref: React.RefObject<T>, callback: (event: MouseEvent) => void): void {
    const listener = (event: MouseEvent | TouchEvent) => {
        if (!ref.current || ref.current.contains(event.target as Node)) return;
        callback(event);
    };

    useEffect(() => {
        document.addEventListener('mousedown', listener);
        document.addEventListener('touchstart', listener, { passive: true }); // for better mobile behavior

        return () => {
            document.removeEventListener('mousedown', listener);
            document.removeEventListener('touchstart', listener);
        };
    }, [ref]);
}
```
This hook uses the `useEffect` hook to add and remove event listeners for 'mousedown' and 'touchstart'. The listener function checks if the click target is outside of the referenced element. If it is, the callback function is called. The cleanup function removes the event listeners when the component unmounts or the ref changes.

The hook uses TypeScript to ensure that the ref is a reference to an HTMLElement and that the callback is a function. It also ensures that the listener is added only once per mount by including it in the dependency array of `useEffect`. The cleanup function properly removes the event listener using the exact same function as the one passed to `addEventListener`, ensuring proper event listener removal.

150 t/s, 344 tokens, 3s, 2%
