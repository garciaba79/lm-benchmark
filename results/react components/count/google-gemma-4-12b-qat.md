# Gemma 4 12B QAT
Model: google/gemma-4-12b-qat
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

Here is the complete code for the React component. I have used a `style` object to handle the layout and styling as requested.

```tsx
import React, { useState } from 'react';

// Define the shape of the component's props
interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  // Initialize state with the prop value (or default 0)
  const [count, setCount] = useState<number>(initialCount);

  // Handler functions
  const handleIncrement = () => {
    setCount((prev) => prev + 1);
  };

  const handleDecrement = () => {
    setCount((prev) => (prev > 0 ? prev - 1 : 0));
  };

  // Inline styles object
  const styles: { [key: string]: React.CSSProperties } = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#f0f2f5',
    },
    heading: {
      fontSize: '5rem',
      margin: '0 0 20px 0',
      color: '#333',
    },
    buttonContainer: {
      display: 'flex',
      gap: '20px',
    },
    button: {
      padding: '10px 25px',
      fontSize: '1.2rem',
      cursor: 'pointer',
      borderRadius: '8px',
      border: 'none',
      transition: 'background-color 0.2s',
    },
    incrementBtn: {
      backgroundColor: '#4caf50',
      color: 'white',
    },
    decrementBtn: {
      backgroundColor: '#f44336',
      color: 'white',
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>{count}</h1>
      <div style={styles.buttonContainer}>
        <button 
          style={{ ...styles.button, ...styles.decrementBtn }} 
          onClick={handleDecrement}
          disabled={count === 0}
        >
          Decrement
        </button>
        <button 
          style={{ ...styles.button, ...styles.incrementBtn }} 
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

### Key Features of this Implementation:

1.  **TypeScript Interfaces**: I defined `CounterProps` to explicitly type the input, ensuring `initialCount` is a number.
2.  **Functional State**: I used the functional update pattern `setCount(prev => ...)` which is the best practice for ensuring the state update is based on the most recent previous value.
3.  **Logic Protection**: The decrement logic `(prev > 0 ? prev - 1 : 0)` ensures the count never drops below zero as requested.
4.  **Accessibility**: I added a `disabled` attribute to the Decrement button when the count is 0, providing a better user experience.
5.  **Styling**: Used a centralized `styles` object. I used the "spread" operator (`...`) to combine the base button styles with specific colors for the Increment and Decrement buttons.
6.  **Layout**: Used Flexbox to ensure the content is perfectly centered in the viewport.

95 t/s, 823 tokens, 9s, 6%
