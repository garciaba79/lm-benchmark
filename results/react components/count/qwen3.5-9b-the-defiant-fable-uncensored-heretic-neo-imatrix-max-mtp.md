# Qwen3.5 9B The Defiant Fable Uncnr Heretic NEO MAX
Model: qwen3.5-9b-the-defiant-fable-uncensored-heretic-neo-imatrix-max-mtp
Test: component count
Created: 11/22/2026, 02:54:45 AM
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
import React from 'react';

interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  const [count, setCount] = React.useState<number>(initialCount);

  const increment = () => setCount((prev) => prev + 1);

  const decrement = () => setCount((prev) => Math.max(0, prev - 1));

  // Basic inline styles for a clean look
  const containerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  };

  const headingStyle: React.CSSProperties = {
    fontSize: '4rem',
    fontWeight: 700,
    margin: '2rem 0',
    color: '#1f2937', // gray-800
  };

  const buttonBaseStyle: React.CSSProperties = {
    padding: '0.75rem 1.5rem',
    fontSize: '1rem',
    fontWeight: 600,
    borderRadius: '0.5rem',
    border: 'none',
    cursor: 'pointer',
    transition: 'background-color 0.2s ease, transform 0.1s ease',
    outline: 'none',
  };

  const incrementStyle: React.CSSProperties = {
    ...buttonBaseStyle,
    backgroundColor: '#3b82f6', // blue-500
    color: 'white',
  };

  const decrementStyle: React.CSSProperties = {
    ...buttonBaseStyle,
    backgroundColor: '#ef4444', // red-500
    color: 'white',
  };

  return (
    <div style={containerStyle}>
      <h1 style={headingStyle}>{count}</h1>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <button onClick={decrement} style={decrementStyle}>
          Decrement
        </button>
        <button onClick={increment} style={incrementStyle}>
          Increment
        </button>
      </div>
    </div>
  );
};

export default Counter;
```

106 t/s, 554 tokens, 5s, 4%
