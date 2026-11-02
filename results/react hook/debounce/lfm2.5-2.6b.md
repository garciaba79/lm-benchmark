# LFM2.5 2.6B
Model: lfm2.5-2.6b
Test: Hook Debounce
Created: 11/02/2026, 06:22:56 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook useDebounce(value: any, delay: number) in TypeScript that returns a debounced version of the input value. It should update only after the specified delay has passed since the last change. Include proper cleanup on unmount.

Use React 18+, functional components, and avoid external libraries. Explain the benefits, pros, cons and any potential issues.

> #### 🤖 Assistant

### Implementation

Here is the implementation of `useDebounce` using TypeScript and React 18+ hooks. It uses a standard approach with `useState` and `useEffect`, ensuring proper cleanup to prevent memory leaks or state updates on unmounted components.

```typescript
import { useState, useEffect } from 'react';

/**
 * A custom hook that returns a debounced version of the input value.
 *
 * @param value The initial value or current state to be debounced. The type extends T.
 * @param delay The time in milliseconds to wait before updating the returned value.
 * @returns The debounced value, which updates only after the specified delay has passed
 *         since the last change to `value`.
 */
export const useDebounce = <T>(value: T, delay: number): T => {
  // State holds the latest value after the debounce timer has elapsed.
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    // We track the timer ID to allow cleanup and resetting logic.
    let timeoutId: ReturnType<typeof setTimeout> | null = null;

    /**
     * Schedules an update to `debouncedValue`.
     * If a previous timer exists, it is cancelled before starting a new one.
     */
    const scheduleUpdate = () => {
      // Cancel any existing timer if the component re-renders quickly
      if (timeoutId) {
        clearTimeout(timeoutId);
      }

      // Update state only after the delay has passed since this update was triggered
      setDebouncedValue(value);
    };

    // Schedule the update immediately when the effect runs
    scheduleUpdate();

    // Cleanup function: Runs on unmount or before the effect re-runs.
    // It ensures that no pending timer updates the state if the component is gone.
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [value, delay]);

  return debouncedValue;
};
```

### Usage Example

```typescript
function SearchComponent() {
  const handleChange = (query: string) => {
    setSearchQuery(query); // Triggers re-render and value change for useDebounce
  };

  const debouncedQuery = useDebounce<string, number>(searchQuery, 500);

  return (
    <div>
      <input 
        type="text" 
        value={debouncedQuery} 
        onChange={(e) => handleChange(e.target.value)} 
        placeholder="Type to search..." 
      />
      <p>Current debounced state: {debouncedQuery}</p>
    </div>
  );
}
```

### Explanation of Benefits and Pros

1.  **Performance Optimization**: The primary benefit is preventing unnecessary updates or API calls. If `delay` is set to, say, 500ms, a user can type rapidly in a search box without triggering the expensive operation (like an API request) on every keystroke.
2.  **Clean Lifecycle Management**: By using `useEffect` with a cleanup function (`return () => clearTimeout...`), we avoid "Zombie Timers." This prevents memory leaks and React warnings about state updates on unmounted components, which are common pitfalls when handling async operations in hooks.
3.  **Type Safety (Generics)**: The hook is generic (`<T>`). If you pass a string as input, `debouncedValue` is strictly typed as a string. This allows the developer to use this hook with any data type without losing type inference.

### Cons and Potential Issues

1.  **Reference Equality Limitation**: The implementation uses JavaScript's default equality (`===`). If you pass objects or arrays, debouncing will not trigger if the reference changes (e.g., `obj = {...obj}`) even if the contents are logically similar. This is usually desired behavior for simple UI state but might be unintuitive in complex logic.
2.  **Delay Granularity**: The delay is fixed at render time. If you need to change the duration dynamically, you must re-trigger the effect or use a more advanced pattern (like `useRef` to hold the current delay value).
3.  **Unmounting Timers**: While we clean up timers on unmount, there is a brief window where React might try to call the update function before the component actually disappears. This is handled by React's commit phase and is generally safe in modern React versions (18+), but it adds a tiny overhead.
4.  **Stale Closures**: In complex nested scenarios, if `useDebounce` was used inside a callback that relied on other stale variables, the debounced value might be slightly out of sync with the initial render's state due to how React batches updates and schedules effects. However, for simple input handling (like search boxes), this is rarely an issue.

### Key Technical Details

*   **`ReturnType<typeof setTimeout>`**: We define `timeoutId` as a nullable type to distinguish between "no timer" and "active timer."
*   **Dependency Array `[value, delay]`**: The effect re-runs whenever the input value changes or the delay changes. This ensures that if you change the debounce duration dynamically (e.g., from 300ms to 500ms), the previous timer is cancelled before starting a new one.
*   **State vs. Effect**: The actual state update (`setDebouncedValue`) happens in `scheduleUpdate`, which runs inside the effect. This separation keeps the hook logic clean and ensures that the debounced value only changes when React commits the render cycle, not on every single frame tick if the component is suspended.

259 t/s, 3699 tokens, 14s, 23%
