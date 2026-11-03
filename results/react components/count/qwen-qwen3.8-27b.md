# Qwen3.8 27B
Model: qwen/qwen3.8-27b
Test: component count
Created: 11/03/2026, 02:21:01 AM
Exported from: LM Studio (via test script)
Context unknown

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

  const handleIncrement = (): void => {
    setCount((prev) => prev + 1);
  };

  const handleDecrement = (): void => {
    setCount((prev) => (prev > 0 ? prev - 1 : 0));
  };

  const headingStyle: React.CSSProperties = {
    fontSize: '4rem',
    textAlign: 'center',
    margin: '2rem 0',
    fontFamily: 'Arial, sans-serif',
    color: '#333',
  };

  const buttonStyle: React.CSSProperties = {
    padding: '0.75rem 1.5rem',
    fontSize: '1rem',
    margin: '0 0.5rem',
    cursor: 'pointer',
    border: 'none',
    borderRadius: '8px',
    backgroundColor: '#4CAF50',
    color: 'white',
    transition: 'background-color 0.2s ease',
  };

  const containerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '2rem',
    backgroundColor: '#f9f9f9',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    width: '300px',
    margin: '2rem auto',
  };

  return (
    <div style={containerStyle}>
      <h1 style={headingStyle}>{count}</h1>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <button
          style={buttonStyle}
          onClick={handleDecrement}
          disabled={count === 0}
        >
          Decrement
        </button>
        <button
          style={{
            ...buttonStyle,
            backgroundColor: '#2196F3',
          }}
          onClick={handleIncrement}
        >
          Increment
        </button>
      </div>
    </div>
  );
};

export default Counter;
```

23 t/s, 551 tokens, 25s
