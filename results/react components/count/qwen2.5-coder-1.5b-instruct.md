# Qwen2.5 Coder 1.5B Instruct
Model: qwen2.5-coder-1.5b-instruct
Test: component count
Created: 11/02/2026, 05:35:23 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a simple React functional component in TypeScript that does the following:

- Accepts a prop called `initialCount` of type number (default to 0 if not provided).
- Displays the current count in a large, centered heading.
- Has two buttons: "Increment" and "Decrement".
- Clicking "Increment" increases the count by 1.
- Clicking "Decrement" decreases the count by 1, but never lets it go below 0.
- Style the component nicely using inline styles or a basic CSS object (no external CSS files or libraries like Tailwind).
- Make sure all props and state are properly typed.
- Follow modern React principles and best practices.

Show the complete component code, including imports.

> #### 🤖 Assistant

```typescript
import React from 'react';

interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  const [count, setCount] = React.useState(initialCount);

  const increment = () => {
    setCount(prevCount => prevCount + 1);
  };

  const decrement = () => {
    if (count > 0) {
      setCount(prevCount => prevCount - 1);
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <h1 style={{ fontSize: '5rem', fontWeight: 'bold', color: '#333' }}>{count}</h1>
      <button onClick={increment}>Increment</button>
      <button onClick={decrement} disabled={count === 0}>
        Decrement
      </button>
    </div>
  );
};

export default Counter;
```

In this solution, we define a functional component `Counter` that accepts an optional prop `initialCount`. The state of the component is managed using React's `useState` hook. We also define two functions, `increment` and `decrement`, to handle the button clicks. The `increment` function simply increments the count by 1, while the `decrement` function decrements it but only if the current count is greater than 0. The component styles are defined using inline styles for simplicity.

324 t/s, 318 tokens, 1s, 6%
