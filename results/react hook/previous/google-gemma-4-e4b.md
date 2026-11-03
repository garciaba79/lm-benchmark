# Gemma 4 E4B
Model: google/gemma-4-e4b
Test: Hook Previous
Created: 11/03/2026, 12:37:41 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is the implementation of the `usePrevious` hook in TypeScript using React 18+ features.

This solution leverages the `useRef` hook to persist a value across renders without triggering re-renders when the stored value changes.

### `usePrevious.ts`

```tsx
import { useRef, useEffect } from 'react';

/**
 * @template T The type of the value being tracked.
 * @description A custom React hook that returns the previous value of a given argument
 *            across renders. It correctly handles the initial render by returning undefined.
 * @param {T} arg The value to track (the current argument).
 * @returns {T | undefined} The value from the previous render, or undefined on the first render.
 */
function usePrevious<T>(arg: T): T | undefined {
  // 1. Create a ref to store the previous value. Initialize it to undefined.
  const ref = useRef<T>();

  // 2. Use useEffect to update the ref *after* the component renders,
  //    capturing the current 'arg' into the stored state (the ref).
  useEffect(() => {
    // When this effect runs, it means the render with the new 'arg' has completed.
    // We store the *current* value of 'arg' into the ref so that on the *next*
    // render, we can access it as the "previous" one.
    ref.current = arg;
  }, [arg]); // Depend on 'arg' to ensure the effect runs whenever 'arg' changes

  // 3. The return value: On any subsequent render, ref.current holds the value
  //    from the previous successful update cycle (the last argument passed).
  //    On the very first render, we need a default or undefined because ref.current
  //    might not have been explicitly set to a useful "previous" state yet,
  //    although in this setup, it will usually hold 'undefined' initially until 
  //    the first useEffect runs and sets it based on the initial argument.

  // To strictly ensure undefined on the very first run *before* the effect runs its course:
  const previousValue = useRef<T | undefined>();
  
  useEffect(() => {
      previousValue.current = ref.current;
  }, [ref]); // This dependency setup is complex to guarantee "undefined" reliably across all React versions/edge cases without an initial state mechanism.

  // A simpler, robust approach: Trust the first call to useEffect handles initialization correctly. 
  // If we rely only on `ref.current` *after* the first render cycle has completed its effects, 
  // it's usually safe enough, but for strict "undefined on first render," a wrapper pattern is cleaner.

  // --- FINAL ROBUST IMPLEMENTATION CHOICE ---
  // We will stick to returning ref.current, as this is the standard pattern, and we initialize the *return* value logic.
  
  let previous: T | undefined;
  if (typeof window !== 'undefined' && ref.current === undefined) {
      // This check helps if the initial argument itself is not what we want to return on render 0.
      previous = undefined as unknown as T | undefined;
  } else {
      previous = ref.current;
  }


  // For true "undefined on first render," we must compare against the original state before any effect runs.
  const finalPreviousRef = useRef<T | undefined>();

  useEffect(() => {
    finalPreviousRef.current = arg;
  }, [arg]); // This sets the value for *next* render

  // On render 0, this hook will return whatever was in finalPreviousRef.current from previous renders (undefined).
  return finalPreviousRef.current as T | undefined;
}

export default usePrevious;
```

### Explanation and Usage Example

The key challenge with `usePrevious` is guaranteeing that on the *very first render*, it returns a predictable "nothing" value (`undefined`), while ensuring on subsequent renders, it accurately reports the value from the *previous* render.

#### How it Works:

1.  **`useRef()`**: We use two refs conceptually (though the implementation simplifies this). The core idea is that `useRef` stores a mutable value that persists across renders without causing re-renders when changed.
2.  **`useEffect(() => { ... }, [arg])`**: This hook runs *after* the component has rendered with the current `arg`. Inside it, we capture this `arg` and store it into our internal ref (`finalPreviousRef.current = arg`). This prepares the value for the **next** render cycle.
3.  **Return Value**: By returning `finalPreviousRef.current`, when the component renders for the first time:
    *   The `useEffect` hook has not yet run its first update cycle based on a previous argument. Therefore, `finalPreviousRef.current` still holds whatever it was initialized to (or is undefined if we handle initialization correctly). This correctly returns `undefined`.
    *   On subsequent renders, the `useEffect` ran last time, storing the value $N-1$ into the ref. When the component re-renders with value $N$, we immediately read that stored value $N-1$ and return it.

#### Example Usage in a Component:

Here is how you would use this hook in a functional component:

```tsx
import React, { useState } from 'react';
import usePrevious from './usePrevious'; // Assuming the file name above

const CounterComponent: React.FC = () => {
  const [count, setCount] = useState<number>(0);
  
  // Use usePrevious to get the count from the last render
  const previousCount = usePrevious(count);

  return (
    <div>
      <h1>UsePrevious Demo</h1>
      <p>Current Count: <strong>{count}</strong></p>
      <p style={{ color: 'green' }}>Previous Count: <strong>{previousCount === undefined ? "N/A (Initial Render)" : String(previousCount)}</strong></p>
      
      <button onClick={() => setCount(c => c + 1)}>
        Increment Count
      </button>
    </div>
  );
};

// To run this, ensure your root App component renders <CounterComponent />
export default CounterComponent;
```

144 t/s, 1391 tokens, 10s
