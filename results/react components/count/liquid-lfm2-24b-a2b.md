# Lfm2 24B A2B
Model: liquid/lfm2-24b-a2b
Test: component count
Created: 11/02/2026, 05:35:23 AM
Exported from: LM Studio (via test script)
Context 16K

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

```tsx
import React, { useState } from 'react';

interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  const [count, setCount] = useState<number>(initialCount);

  const increment = () => setCount(prev => prev + 1);
  const decrement = () => setCount(prev => Math.max(prev - 1, 0));

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        fontFamily: 'Arial, sans-serif',
      }}
    >
      <h1
        style={{
          fontSize: '3rem',
          marginBottom: '2rem',
          color: '#333',
        }}
      >
        Count: {count}
      </h1>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <button
          onClick={increment}
          style={{
            padding: '0.5rem 1rem',
            fontSize: '1rem',
            cursor: 'pointer',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
          }}
        >
          Increment
        </button>
        <button
          onClick={decrement}
          style={{
            padding: '0.5rem 1rem',
            fontSize: '1rem',
            cursor: 'pointer',
            backgroundColor: '#f44336',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
          }}
        >
          Decrement
        </button>
      </div>
    </div>
  );
};

export default Counter;
```

This component:
- Uses TypeScript for type safety.
- Accepts an optional `initialCount` prop with a default value of 0.
- Manages state using React hooks (`useState`).
- Ensures the count never goes below 0 when decrementing.
- Styles everything inline for simplicity and clarity.

111 t/s, 492 tokens, 5s, 4%
