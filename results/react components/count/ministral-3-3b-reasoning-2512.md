# Ministral 3 3B Reasoning 2512
Model: ministral-3-3b-reasoning-2512
Test: component count
Created: 11/02/2026, 05:35:23 AM
Exported from: LM Studio (via test script)
Context 32K

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

Here is the complete React functional component in TypeScript that meets all the specified requirements:

```tsx
import React, { useState } from 'react';

interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  const [count, setCount] = useState<number>(initialCount);

  const increment = () => {
    setCount(prevCount => prevCount + 1);
  };

  const decrement = () => {
    setCount(prevCount => (prevCount > 0 ? prevCount - 1 : 0));
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      margin: '0'
    }}>
      <h1 style={{
        fontSize: '3rem',
        color: '#333',
        marginBottom: '20px'
      }}>
        {count}
      </h1>
      <div style={{
        display: 'flex',
        gap: '20px'
      }}>
        <button onClick={increment} style={{
          padding: '10px 20px',
          fontSize: '1rem',
          cursor: 'pointer',
          backgroundColor: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '4px'
        }}>
          Increment
        </button>
        <button onClick={decrement} style={{
          padding: '10px 20px',
          fontSize: '1rem',
          cursor: 'pointer',
          backgroundColor: '#f44336',
          color: 'white',
          border: 'none',
          borderRadius: '4px'
        }}>
          Decrement
        </button>
      </div>
    </div>
  );
};

export default Counter;
```

This component:
- Accepts an optional `initialCount` prop with a default of 0.
- Manages state for the count using `useState`.
- Displays the count in a large, centered heading (h1) with font size 3rem.
- Includes two buttons: "Increment" and "Decrement".
- Increments the count by 1 when "Increment" is clicked.
- Decrements the count by 1 but ensures it never goes below 0 when "Decrement" is clicked.
- Uses inline styles for basic styling without external libraries.
- Properly types all props and state in TypeScript.

214 t/s, 1835 tokens, 9s, 6%
