# Qwen3.6 35B A3B
Model: qwen/qwen3.6-35b-a3b
Test: Hook Click Outside
Created: 11/22/2026, 12:44:09 PM
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

```typescript
import { useEffect, useCallback } from 'react';

type ClickOutsideCallback = (event: MouseEvent | TouchEvent) => void;

export function useClickOutside<T extends HTMLElement>(
  ref: React.RefObject<T | null>,
  callback: ClickOutsideCallback
): void {
  const handleClickOutside = useCallback(
    (event: MouseEvent | TouchEvent) => {
      if (!ref.current) {
        return;
      }

      const target = event.target as Node;

      // Check if the click target is outside the referenced element
      if (!ref.current.contains(target)) {
        callback(event);
      }
    },
    [ref, callback]
  );

  useEffect(() => {
    const element = ref.current;
    if (!element) {
      return;
    }

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('touchstart', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('touchstart', handleClickOutside);
    };
  }, [ref, handleClickOutside]);
}
```

48 t/s, 244 tokens, 5s, 3%
