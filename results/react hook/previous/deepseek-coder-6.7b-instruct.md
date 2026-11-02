# Deepseek Coder 6.7B Instruct
Model: deepseek-coder-6.7b-instruct
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is an implementation for your request using `useRef` and `React.MutableRefObject` in TypeScript. This custom hook will return the previous value of a generic type T from the last render. It handles initial renders correctly by returning undefined on first render as there would be no "previous" state yet:

```tsx
import React, { useEffect, useRef } from 'react';

function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();
  
  // Store current value in ref on every render
  useEffect(() => {
    ref.current = value;
  }, [value]);
  
  return ref.current;
}
```
This hook works by creating a `React.MutableRefObject` that is initialized with the given initialValue and whose .current property is mutable. The returned object will persist for the full lifetime of the component, unlike useState which resets on every render. 

In this case we are using it to store the previous value from last render in a ref called `ref`. We then return that stored value as our "previous" state. When the input (value) changes, the effect runs and updates the current property of the ref with the new value. This way, on every subsequent render, we have access to the previously rendered value via `ref.current`.

138 t/s, 306 tokens, 2s, 3%
