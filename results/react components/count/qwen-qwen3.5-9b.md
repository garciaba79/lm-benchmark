# Qwen3.5 9B
Model: qwen/qwen3.5-9b
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

Here is the complete React functional component in TypeScript. It uses standard hooks, proper type definitions, and a CSS-in-JS object for styling.

```tsx
import React, { useState } from 'react';

// 1. Define the Props Interface
interface CountDisplayProps {
  initialCount?: number; // Optional prop that defaults to 0 if not provided
}

// 2. Define the Styles using a simple CSS object
const styles = {
  container: {
    fontFamily: '"Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    textAlign: 'center',
    padding: '40px',
    backgroundColor: '#f5f5f5', // Light grey background
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    maxWidth: '300px',
    margin: 'auto',
  },
  heading: {
    fontSize: '4rem', // Large heading
    margin: '20px 0',
    color: '#333',
    fontWeight: 'bold',
  },
  buttonContainer: {
    display: 'flex',
    gap: '10px',
    justifyContent: 'center',
    marginTop: '20px',
  },
  button: (type: 'increment' | 'decrement') => ({
    padding: '10px 20px',
    fontSize: '1rem',
    cursor: 'pointer',
    border: 'none',
    borderRadius: '6px',
    color: 'white',
    fontWeight: 'bold',
    transition: 'opacity 0.2s',
    opacity: type === 'decrement' ? '1' : '1', // Ensure both are visible
    backgroundColor: type === 'increment' ? '#4CAF50' : '#FF9800',
  }),
};

// 3. The Component
const CountDisplay: React.FC<CountDisplayProps> = ({ initialCount = 0 }) => {
  // Initialize state with the prop value
  const [count, setCount] = useState<number>(initialCount);

  // Increment Handler
  const handleIncrement = () => {
    setCount((prevCount) => prevCount + 1);
  };

  // Decrement Handler: Math.max ensures it never goes below 0
  const handleDecrement = () => {
    setCount((prevCount) => Math.max(0, prevCount - 1));
  };

  return (
    <div style={styles.container}>
      {/* Display the count */}
      <h1 style={styles.heading}>{count}</h1>

      {/* Button Controls */}
      <div style={styles.buttonContainer}>
        <button 
          onClick={handleDecrement} 
          style={styles.button('decrement')}
          aria-label="Decrement Count"
        >
          Decrement
        </button>
        
        <button 
          onClick={handleIncrement} 
          style={styles.button('increment')}
          aria-label="Increment Count"
        >
          Increment
        </button>
      </div>
    </div>
  );
};

export default CountDisplay;
```

121 t/s, 1619 tokens, 14s, 11%
