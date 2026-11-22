# Qwen3.6 35B A3B
Model: qwen/qwen3.6-35b-a3b
Test: component count
Created: 11/22/2026, 12:44:02 PM
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

Here is the complete code for the `Counter` component. It includes necessary imports, TypeScript interfaces, state management, and inline styling.

```tsx
import React, { useState } from 'react';

// Define the props interface
interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  // State to track the current count, initialized with the prop
  const [count, setCount] = useState<number>(initialCount);

  // Styles object for cleaner code organization
  const styles = {
    container: {
      fontFamily: 'sans-serif',
      textAlign: 'center' as const,
      padding: '2rem',
      maxWidth: '400px',
      margin: '0 auto',
      border: '1px solid #e0e0e0',
      borderRadius: '8px',
      backgroundColor: '#f9f9f9',
    },
    heading: {
      fontSize: '4rem',
      margin: '1.5rem 0',
      color: '#333',
    },
    buttonGroup: {
      display: 'flex',
      justifyContent: 'center',
      gap: '1rem',
    },
    button: {
      padding: '10px 20px',
      fontSize: '1rem',
      cursor: 'pointer',
      backgroundColor: '#007bff',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      transition: 'background-color 0.2s',
    },
    decrementButton: {
      backgroundColor: '#dc3545', // Red for decrement
    },
  };

  const handleIncrement = () => {
    setCount((prev) => prev + 1);
  };

  const handleDecrement = () => {
    setCount((prev) => Math.max(prev - 1, 0));
  };

  return (
    <div style={styles.container}>
      <h1>Counter</h1>
      
      {/* Display the count in a large, centered heading */}
      <h2 style={styles.heading}>
        {count}
      </h2>

      <div style={styles.buttonGroup}>
        {/* Decrement Button */}
        <button 
          onClick={handleDecrement} 
          style={{ ...styles.button, ...styles.decrementButton }}
        >
          Decrement
        </button>

        {/* Increment Button */}
        <button 
          onClick={handleIncrement} 
          style={styles.button}
        >
          Increment
        </button>
      </div>
    </div>
  );
};

export default Counter;
```

48 t/s, 621 tokens, 13s, 5%
