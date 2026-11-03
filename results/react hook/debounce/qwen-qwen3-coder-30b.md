# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: Hook Debounce
Created: 11/03/2026, 02:57:46 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook useDebounce(value: any, delay: number) in TypeScript that returns a debounced version of the input value. It should update only after the specified delay has passed since the last change. Include proper cleanup on unmount.

Use React 18+, functional components, and avoid external libraries. Explain the benefits, pros, cons and any potential issues.

> #### 🤖 Assistant

```typescript
import { useState, useEffect, useRef } from 'react';

/**
 * Custom hook that returns a debounced version of a value
 * @param value - The value to debounce
 * @param delay - Delay in milliseconds
 * @returns Debounced value that updates after specified delay
 */
function useDebounce<T>(value: T, delay: number): T {
  // State to hold the debounced value
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  
  // Ref to store the timeout ID
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    // Clear the previous timeout if it exists
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Set a new timeout to update the debounced value
    timeoutRef.current = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cleanup function to clear timeout on unmount or when dependencies change
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [value, delay]); // Dependencies array ensures effect runs when value or delay changes

  return debouncedValue;
}

export default useDebounce;
```

## Usage Example:

```typescript
import React, { useState } from 'react';
import useDebounce from './useDebounce';

function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  // This will only trigger after 500ms of inactivity
  useEffect(() => {
    if (debouncedSearchTerm) {
      console.log('Searching for:', debouncedSearchTerm);
      // Perform search API call here
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
}
```

## Benefits:

1. **Performance Optimization**: Reduces the number of expensive operations (API calls, computations) by delaying them until after user stops typing or interacting
2. **Resource Efficiency**: Prevents overwhelming the browser with rapid updates
3. **User Experience**: Provides smoother interactions, especially for search inputs and real-time filtering
4. **Clean Implementation**: Simple, reusable hook that follows React best practices

## Pros:

- **No External Dependencies**: Pure React implementation
- **Type Safety**: Full TypeScript support with generic types
- **Automatic Cleanup**: Proper cleanup of timeouts prevents memory leaks
- **Flexible**: Works with any data type (string, number, object, etc.)
- **React 18+ Compatible**: Uses modern React hooks and patterns
- **Dependency Management**: Correctly handles changing delay values

## Cons:

1. **Additional State**: Introduces an extra state variable and effect
2. **Potential Delay**: Users might experience a slight delay in seeing results
3. **Memory Overhead**: Temporary timeout references are created for each update
4. **Complexity**: Slightly more complex than simple state management

## Potential Issues:

1. **Initial Value**: The debounced value will initially be the same as the input value, which might cause a flash of unfiltered content
2. **Dependency Array**: If delay is not included in dependencies, changing delay won't reset the timeout properly
3. **Immediate Updates**: During rapid changes, the final value might not be immediately reflected (intentional behavior)
4. **Memory Leaks**: Without proper cleanup, timeouts could accumulate and cause memory leaks
5. **Edge Cases**: Very short delays (< 10ms) might not provide meaningful debouncing

## Alternative Implementation with Immediate Update Option:

```typescript
function useDebounce<T>(value: T, delay: number, immediate: boolean = false): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // If immediate is true, update immediately and then debounce subsequent updates
    if (immediate && value !== debouncedValue) {
      setDebouncedValue(value);
      timeoutRef.current = setTimeout(() => {
        setDebouncedValue(value);
      }, delay);
    } else {
      timeoutRef.current = setTimeout(() => {
        setDebouncedValue(value);
      }, delay);
    }

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [value, delay, immediate, debouncedValue]);

  return debouncedValue;
}
```

This hook is particularly useful for search inputs, filtering lists, and any scenario where you want to limit the frequency of updates or API calls based on user interaction.

61 t/s, 1035 tokens, 17s
