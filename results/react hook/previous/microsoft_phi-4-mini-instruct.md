# Microsoft Phi 4 Mini Instruct
Model: microsoft_phi-4-mini-instruct
Test: Hook Previous
Created: 11/02/2026, 07:20:09 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called usePrevious in TypeScript that takes a value of generic type T and returns the previous value from the last render. It should work with any type and handle initial renders correctly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

import { useRef } from 'react';

const usePrevious = <T>(value: T): T | undefined => {
  const ref = useRef<any>();

  // On every render we set the current value to our `ref`, and then return its previous *current* state.
  React.useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
};

export default usePrevious;

193 t/s, 88 tokens, 0s, 1%
