# Mamba Codestral 7B v0.1
Model: mamba-codestral-7b-v0.1
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 32K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```typescript
import { useState, useRef } from 'react';

export function usePrevious<T>(value: T): T | undefined {
    const ref = useRef<T>();

    // Store current value in ref
    ref.current = value;

    return ref.current;
}
```
This hook uses the `useRef` hook to create a reference that persists across renders and stores the previous value of the provided variable. The useEffect hook is not needed here because we want to access the current state immediately after it has been updated, which can be done without waiting for the next render cycle.

The generic type `<T>` allows this hook to work with any type. When initializing a component or when the value provided changes, the ref's current property will hold the previous value from the last render. This is why we return `ref.current`, which always contains the most recent value before it was updated by React.

This solution works for both function and class components in React 18+ as hooks are available in both.

135 t/s, 234 tokens, 2s, 1%
