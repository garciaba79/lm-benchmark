# Gemma 4 E4B
Model: google/gemma-4-e4b
Test: component count
Created: 11/03/2026, 12:36:48 AM
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

Here is the complete, self-contained functional component written in TypeScript that meets all the specified requirements.

```tsx
import React, { useState, useCallback } from 'react';

// 1. Define the Props interface for type safety
interface CounterProps {
  initialCount?: number; // Optional prop with a default value handled by the component logic
}

/**
 * A simple counter component that displays a count and allows incrementing/decrementing.
 * @param props The component props, including an optional initialCount.
 */
const Counter: React.FC<CounterProps> = ({ 
  initialCount = 0 // Setting the default value in the destructuring is cleaner here
}) => {
  // State definition: Use useState with proper typing
  const [count, setCount] = useState<number>(initialCount);

  // Handler for incrementing the count
  const handleIncrement = useCallback(() => {
    setCount(prevCount => prevCount + 1);
  }, []); // Dependencies array is empty as it only uses the previous state (via functional update)

  // Handler for decrementing the count, ensuring it doesn't go below zero
  const handleDecrement = useCallback(() => {
    setCount(prevCount => (prevCount > 0 ? prevCount - 1 : 0));
  }, []);

  // Styles definition using basic JS objects
  const styles: React.CSSProperties = {
    container: {
      fontFamily: 'Arial, sans-serif',
      textAlign: 'center',
      padding: '40px',
      maxWidth: '600px',
      margin: '50px auto', // Center the whole component on the page
      border: '1px solid #ccc',
      borderRadius: '10px',
      boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    },
    heading: {
      fontSize: '5rem', // Large size
      margin: '20px 0',
      color: '#333'};
    const buttonContainer: React.CSSProperties = {
        display: 'flex',
        justifyContent: 'space-around',
        marginTop: '30px',
    };
    const buttonStyle: React.CSSProperties = {
        padding: '12px 25px',
        fontSize: '1.2rem',
        cursor: 'pointer',
        border: 'none',
        borderRadius: '8px',
        transition: 'background-color 0.2s ease',
    };

  // Determine button styles based on the current count for visual feedback
  const incrementButtonStyle: React.CSSProperties = {
      ...buttonStyle,
      backgroundColor: '#4CAF50', // Green
      color: 'white',
      ':hover': { backgroundColor: '#45a049' } // Note: Pseudo-selectors need inline state management or just rely on the main style if using true CSS files. For simplicity in pure inline styles, we stick to hover effects via React's event handlers or simplified styling.
  };

  const decrementButtonStyle: React.CSSProperties = {
      ...buttonStyle,
      backgroundColor: '#f44336', // Red
      color: 'white',
      ':hover': { backgroundColor: '#da190b' } 
  }


  return (
    <div style={styles.container}>
      {/* Displaying the count */}
      <h1 style={styles.heading}>{count}</h1>

      <div style={styles.buttonContainer}>
        {/* Increment Button */}
        <button
          onClick={handleIncrement}
          style={{ ...styles.buttonStyle, backgroundColor: '#4CAF50', color: 'white' }}
          onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#45a049'}
          onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#4CAF50'}
        >
          Increment
        </button>

        {/* Decrement Button */}
        <button
          onClick={handleDecrement}
          style={{ ...styles.buttonStyle, backgroundColor: '#f44336', color: 'white' }}
          onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#da190b'}
          onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#f44336'}
        >
          Decrement
        </button>
      </div>
    </div>
  );
};

export default Counter;

// Example Usage (How you would use this component in App.tsx):
/*
import React from 'react';
import Counter from './Counter';

const App: React.FC = () => {
  return (
    <div className="App">
      <h1>React TypeScript Counter Demo</h1>
      <h2>Starting at 10:</h2>
      <Counter initialCount={10} />

      <hr style={{ margin: '50px auto', width: '80%' }}/>

      <h2>Starting at default (0):</h2>
      <Counter />
    </div>
  );
};

export default App;
*/
```

142 t/s, 1153 tokens, 8s
