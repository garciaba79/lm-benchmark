# Gemma 4 E2B
Model: google/gemma-4-e2b
Test: component count
Created: 11/15/2026, 09:43:19 PM
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

Here is the complete, well-typed React functional component written in TypeScript that meets all the requirements.

```tsx
import React, { useState, useMemo } from 'react';

// 1. Define the props interface for type safety
interface CounterProps {
  /** The initial value for the counter. Defaults to 0. */
  initialCount?: number;
}

/**
 * A simple interactive counter component.
 * @param {CounterProps} props - The component props.
 */
const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  // 2. State management using the useState hook
  const [count, setCount] = useState<number>(initialCount);

  // 3. Event handlers for state updates
  const handleIncrement = () => {
    setCount(prevCount => prevCount + 1);
  };

  const handleDecrement = () => {
    // Ensure the count does not go below 0
    setCount(prevCount => Math.max(0, prevCount - 1));
  };

  // 4. Inline styling for a nice presentation
  const containerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh', // Make it full height for centering
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f4f7f6',
  };

  const headingStyle: React.CSSProperties = {
    fontSize: '4em',
    margin: '20px 0',
    color: '#333',
    fontWeight: 'bold',
  };

  const buttonStyle: React.CSSProperties = {
    padding: '10px 20px',
    margin: '10px',
    fontSize: '1em',
    cursor: 'pointer',
    border: 'none',
    borderRadius: '5px',
    color: 'white',
    backgroundColor: '#007bff',
    transition: 'background-color 0.3s ease',
  };

  const incrementButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#28a745', // Green for increment
  };

  const decrementButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#dc3545', // Red for decrement
  };

  return (
    <div style={containerStyle}>
      <h1 style={headingStyle}>
        {count}
      </h1>
      <div>
        {/* Increment Button */}
        <button 
          onClick={handleIncrement} 
          style={incrementButtonStyle}
        >
          Increment
        </button>
        
        {/* Decrement Button */}
        <button 
          onClick={handleDecrement} 
          style={decrementButtonStyle}
        >
          Decrement
        </button>
      </div>
    </div>
  );
};

export default Counter;

// Example Usage (for testing purposes, typically in App.tsx)
/*
import React from 'react';
import Counter from './Counter'; // Assuming you saved the file as Counter.tsx

const App: React.FC = () => {
  return (
    <div>
      <Counter initialCount={10} />
      <br/>
      <Counter /> // Uses default count of 0
    </div>
  );
};

export default App;
*/
```

191 t/s, 781 tokens, 4s
