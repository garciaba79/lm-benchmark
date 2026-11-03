# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: component count
Created: 11/03/2026, 02:57:17 AM
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

  const handleIncrement = () => {
    setCount(prevCount => prevCount + 1);
  };

  const handleDecrement = () => {
    setCount(prevCount => Math.max(0, prevCount - 1));
  };

  const counterStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f5f5f5',
  };

  const headingStyle: React.CSSProperties = {
    fontSize: '4rem',
    margin: '2rem 0',
    color: '#333',
  };

  const buttonStyle: React.CSSProperties = {
    padding: '0.75rem 1.5rem',
    margin: '0.5rem',
    fontSize: '1.2rem',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    backgroundColor: '#007bff',
    color: 'white',
    transition: 'background-color 0.2s',
  };

  const buttonHoverStyle: React.CSSProperties = {
    backgroundColor: '#0056b3',
  };

  return (
    <div style={counterStyle}>
      <h1 style={headingStyle}>{count}</h1>
      <div>
        <button 
          style={buttonStyle} 
          onClick={handleIncrement}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#0056b3')}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#007bff')}
        >
          Increment
        </button>
        <button 
          style={buttonStyle} 
          onClick={handleDecrement}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#dc3545')}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#dc3545')}
        >
          Decrement
        </button>
      </div>
    </div>
  );
};

export default Counter;
```

62 t/s, 505 tokens, 8s
