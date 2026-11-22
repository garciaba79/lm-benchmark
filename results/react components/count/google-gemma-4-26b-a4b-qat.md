# Gemma 4 26B A4B QAT
Model: google/gemma-4-26b-a4b-qat
Test: component count
Created: 11/22/2026, 03:07:48 AM
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

Here is a complete, single-file solution. I have used a CSS object for styling to keep the component self-contained and clean.

```tsx
import React, { useState } from 'react';

// 1. Define the interface for the component props
interface CounterProps {
  initialCount?: number; // Optional prop, defaults to 0
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  // 2. Define state with explicit type number
  const [count, setCount] = useState<number>(initialCount);

  // 3. Logic functions
  const handleIncrement = () => {
    setCount((prev) => prev + 1);
  };

  const handleDecrement = () => {
    setCount((prev) => (prev > 0 ? prev - 1 : 0));
  };

  // 4. Inline Styles Object
  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column' as 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '300px',
      width: '300px',
      margin: '40px auto',
      padding: '20px',
      borderRadius: '12px',
      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
      backgroundColor: '#ffffff',
      fontFamily: 'sans-serif',
    },
    heading: {
      fontSize: '48px',
      margin: '20px 0',
      color: '#333',
    },
    buttonGroup: {
      display: 'flex',
      gap: '10px',
    },
    button: {
      padding: '10px 20px',
      fontSize: '16px',
      cursor: 'pointer',
      borderRadius: '6px',
      border: 'none',
      transition: 'opacity 0.2s',
      color: 'white',
    },
    incrementBtn: {
      backgroundColor: '#4CAF50',
    },
    decrementBtn: {
      backgroundColor: '#f44336',
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>{count}</h1>
      
      <div style={styles.buttonGroup}>
        <button 
          onClick={handleDecrement} 
          style={{ ...styles.button, ...styles.decrementBtn }}
        >
          Decrement
        </button>
        
        <button 
          onClick={handleIncrement} 
          style={{ ...styles.button, ...styles.incrementBtn }}
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

1.  **TypeScript Interfaces**: Used `interface CounterProps` to define the shape of the props. The `initialCount` is marked as optional (`?`) with a default parameter in the destructuring.
2.  **State Management**: Used the `useState` hook with an explicit type `<number>`. I used the functional update pattern `setCount(prev => ...)` which is a best practice when the new state depends on the previous state.
3.  **Business Logic**: The `handleDecrement` function uses a ternary operator to ensure the count never drops below zero, fulfilling your specific requirement.
4.  **Styling**:
    *   Used a `styles` object to keep the JSX clean and readable.
    *   Used `flexbox` to ensure the content is perfectly centered.
    *   Applied a "card" design with a subtle shadow and rounded corners for a modern look.
5.  **Modern Patterns**:
    *   Used `React.FC` (Functional Component) type for the component definition.
    *   Destructured props directly in the function signature.
    *   Ensured all event handlers are defined clearly.

### How to use it in your App:
```tsx
import Counter from './Counter';

function App() {
  return (
    <div>
      {/* Uses default value (0) */}
      <Counter />
      
      {/* Starts at 10 */}
      <Counter initialCount={10} />
    </div>
  );
}
```

55 t/s, 994 tokens, 18s, 7%
