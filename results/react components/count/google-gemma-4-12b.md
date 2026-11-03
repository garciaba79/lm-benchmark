# Gemma 4 12B
Model: google/gemma-4-12b
Test: component count
Created: 11/03/2026, 01:00:56 AM
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

Here is a clean, production-ready implementation using React hooks and TypeScript.

```tsx
import React, { useState } from 'react';

// Define the interface for the component props
interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  // State managed with type inference from the initial value
  const [count, setCount] = useState<number>(initialCount);

  // Logic handlers
  const handleIncrement = () => {
    setCount((prev) => prev + 1);
  };

  const handleDecrement = () => {
    setCount((prev) => Math.max(0, prev - 1));
  };

  // Inline styles object
  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      backgroundColor: '#f4f7f6',
    },
    heading: {
      fontSize: '5rem',
      margin: '0 0 20px 0',
      color: '#333',
    },
    buttonContainer: {
      display: 'flex',
      gap: '15px',
    },
    button: (color: string): React.CSSProperties => ({
      padding: '12px 24px',
      fontSize: '1.1rem',
      cursor: 'pointer',
      border: 'none',
      borderRadius: '8px',
      backgroundColor: color,
      color: '#fff',
      transition: 'opacity 0.2s ease',
    }),
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>{count}</h1>
      <div style={styles.buttonContainer}>
        <button 
          onClick={handleDecrement} 
          style={styles.button('#e74c3c')}
          aria-label="Decrement count"
        >
          Decrement
        </button>
        <button 
          onClick={handleIncrement} 
          style={styles.button('#2ecc71')}
          aria-label="Increment count"
        >
          Increment
        </button>
      </div>
    </div>
  );
};

export default Counter;
```

### Key Features of this Implementation:

1.  **TypeScript Excellence**: 
    *   Defined a `CounterProps` interface to ensure type safety for props.
    *   Explicitly typed the state hook as `<number>`.
2.  **State Logic**:
    *   Used the **functional update pattern** (`setCount(prev => ...)`). This is a best practice when the new state depends on the previous state, as it guarantees consistency during rapid consecutive clicks.
3.  **Boundary Logic**: 
    *   Implemented `Math.max(0, prev - 1)` to cleanly ensure the counter never drops below zero without needing extra `if` statements.
4.  **Clean Styling**:
    *   Used a structured `styles` object to keep the JSX clean and readable.
    *   Included basic styling to center the content both vertically and horizontally on the page.
5.  **Accessibility**: 
    *   Added `aria-label` attributes to buttons for better screen reader support.
6.  **Default Props**:
    *   Utilized ES6 default parameters (`initialCount = 0`) to handle cases where no prop is passed.

82 t/s, 816 tokens, 10s
