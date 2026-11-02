# LFM2.5 2.6B
Model: lfm2.5-2.6b
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

```typescript
import React, { useState } from 'react';

// Define the props interface for strict typing
interface CountProps {
  initialCount?: number;
}

const CountDisplay: React.FC<CountProps> = ({ initialCount }) => {
  // Initialize state with the provided prop or default to 0
  const [count, setCount] = useState<number>(initialCount);

  // Function to increment the count
  const handleIncrement = () => {
    setCount(prev => prev + 1);
  };

  // Function to decrement the count, ensuring it never goes below 0
  const handleDecrement = () => {
    setCount(prev => Math.max(0, prev - 1));
  };

  return (
    <div style={styles.container}>
      {/* Large, centered heading */}
      <h2 style={styles.heading}>{count}</h2>

      {/* Container for buttons to center them horizontally */}
      <div style={styles.buttonGroup}>
        <button
          onClick={handleIncrement}
          style={styles.button}
          aria-label="Increase count"
        >
          Increase
        </button>
        <button
          onClick={handleDecrement}
          style={styles.button}
          aria-label="Decrease count"
        >
          Decrease
        </button>
      </div>
    </div>
  );
};

// Basic CSS object for styling (no external files)
const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh', // Ensure it takes up the full viewport height
    backgroundColor: '#f4f7fa',
    padding: '20px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
  },
  heading: {
    fontSize: '3rem', // Large text size
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: '30px',
  },
  buttonGroup: {
    display: 'flex',
    gap: '15px',
  },
  button: {
    padding: '14px 24px',
    fontSize: '1rem',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.2s ease,
    // Styling for the Increment Button (Green)
    backgroundColor: '#27ae60', 
    color: 'white',
    border: 'none',
  }
};

export default CountDisplay;
```

287 t/s, 2360 tokens, 8s, 15%
