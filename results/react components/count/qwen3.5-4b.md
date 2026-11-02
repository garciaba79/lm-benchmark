# Qwen3.5 4B
Model: qwen3.5-4b
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

// Define the props interface for type safety
interface CounterProps {
  initialCount?: number;
}

/**
 * A simple counter component that accepts an optional starting value.
 */
const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  // State to track the current count, initialized with the prop
  const [count, setCount] = useState<number>(initialCount);

  // Handler for incrementing
  const handleIncrement = () => {
    setCount((prev) => prev + 1);
  };

  // Handler for decrementing (with floor at 0)
  const handleDecrement = () => {
    setCount((prev) => Math.max(0, prev - 1));
  };

  return (
    <div style={styles.container}>
      {/* Large centered heading */}
      <h1 style={styles.heading}>{count}</h1>

      <div style={styles.buttonGroup}>
        <button onClick={handleIncrement} style={styles.button}>
          Increment (+)
        </button>
        
        <button onClick={handleDecrement} style={styles.button}>
          Decrement (-)
        </button>
      </div>
    </div>
  );
};

// CSS-in-JS object for styling
const styles: { [key: string]: React.CSSProperties } = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh', // Full viewport height
    backgroundColor: '#f3f4f6',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  heading: {
    fontSize: '5rem',
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: '40px',
    margin: '0 auto', // Center text horizontally
  },
  buttonGroup: {
    display: 'flex',
    gap: '20px',
  },
  button: {
    padding: '15px 30px',
    fontSize: '1.2rem',
    fontWeight: '600',
    color: '#ffffff',
    backgroundColor: '#3b82f6', // Blue-500
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.2s ease',
  },
};

export default Counter;
```

176 t/s, 1137 tokens, 7s, 8%
