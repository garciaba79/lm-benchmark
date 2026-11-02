# Ministral 3 8B Instruct 2512
Model: ministral-3-8b-instruct-2512
Test: Hook Debounce
Created: 11/02/2026, 06:22:56 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook useDebounce(value: any, delay: number) in TypeScript that returns a debounced version of the input value. It should update only after the specified delay has passed since the last change. Include proper cleanup on unmount.

Use React 18+, functional components, and avoid external libraries. Explain the benefits, pros, cons and any potential issues.

> #### 🤖 Assistant

# Custom `useDebounce` Hook in TypeScript

Here's a complete implementation of a `useDebounce` hook that works with React 18+ functional components:

```typescript
import { useState, useEffect } from 'react';

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    // Set the timer for each new value
    const timerId = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Return cleanup function to clear the timer if component unmounts or value changes
    return () => {
      clearTimeout(timerId);
    };
  }, [value, delay]); // Only re-run effect if value or delay changes

  return debouncedValue;
}

export default useDebounce;
```

## Usage Example

```typescript
import React from 'react';
import useDebounce from './useDebounce';

const SearchComponent = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  // Use debouncedSearchTerm for API calls or other expensive operations
  React.useEffect(() => {
    if (debouncedSearchTerm.length > 2) {
      console.log('Performing search with:', debouncedSearchTerm);
      // Your API call here
    }
  }, [debouncedSearchTerm]);

  return (
    <input
      type="text"
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
      placeholder="Search..."
    />
  );
};
```

## Benefits

1. **Performance Optimization**: Prevents unnecessary re-renders or API calls during rapid input changes.
2. **Clean Architecture**: Encapsulates debouncing logic in a reusable hook.
3. **Type Safety**: Proper TypeScript typing ensures type safety for any value type.
4. **No External Dependencies**: Pure React implementation without external libraries.
5. **Memory Safe**: Proper cleanup of timers prevents memory leaks.

## Pros

1. **Reusable**: Can be used across multiple components with different delay values.
2. **Flexible**: Works with any type of input value (string, object, etc.).
3. **React 18 Compatible**: Uses modern React features and patterns.
4. **Controlled Delay**: Explicit delay parameter gives fine-grained control over debouncing behavior.

## Cons/Potential Issues

1. **Initial Render Lag**: The first render might show the initial value immediately without any delay.
2. **Timer Management**: Must properly clean up timers to avoid memory leaks (handled in this implementation).
3. **Dependency Array**: The effect depends on both `value` and `delay`, which is correct but worth noting.
4. **Edge Cases**: Very rapid successive changes might still trigger multiple debounced updates if the delay isn't long enough.

## Advanced Version with Initial Value Handling

For better UX where you want to show the initial value immediately:

```typescript
function useDebounce<T>(value: T, delay: number): [T, boolean] {
  const [debouncedValue, setDebouncedValue] = useState(value);
  const [isInitialRender, setIsInitialRender] = useState(true);

  useEffect(() => {
    if (isInitialRender) {
      setIsInitialRender(false);
      return;
    }

    const timerId = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timerId);
  }, [value, delay]);

  return [debouncedValue, isInitialRender];
}
```

This version returns a tuple where the second value indicates if it's the initial render.

## Testing Considerations

When testing this hook:
1. Test with rapid successive changes
2. Verify cleanup works on unmount
3. Check behavior with different delay values
4. Ensure type safety for various input types

The implementation follows React best practices by properly managing side effects and dependencies, and provides a clean abstraction for debouncing functionality in your components.

122 t/s, 870 tokens, 7s, 9%
